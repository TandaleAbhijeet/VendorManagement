
from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# ======================================== vendor View =============================

class GetCreatevendor(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="The Create Vendor API, Create a new Vendor ",
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'contact_details': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
                'vendor_code': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['name', 'contact_details', 'address', 'vendor_code'],
        ),
        responses={
            201: "vendor Created successfully",
            400: "Bad request",
            500: "Internal server error",
        }
    )
    def post(self,request):
        
        try:
            data = request.data
            seralizer = vendorSerailzer(data=data)
            print('wend')
            if seralizer.is_valid():
                seralizer.save()
                return Response({'status':status.HTTP_201_CREATED, 'data':seralizer.data, 'responseMessage': 'vendor Created successfully'},status=status.HTTP_201_CREATED)
            return Response({'status':status.HTTP_400_BAD_REQUEST,  'responseMessage': seralizer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,  'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
            operation_summary="The Get vendor API, provide the list of all vendors",
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ],
        responses={
            200: "Data found Successfully",
            500: "Internal server error",
        }
    )
    def get(self,request):
        try:
            vendorDetails = Vendor.objects.all()
            seralizer = vendorDeatailsSeralizer(vendorDetails, many=True)     
            return Response({'status': status.HTTP_200_OK, 'data': seralizer.data, 'responseMessage': 'Data found Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,  'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    


class VendorOpration(APIView):

    @swagger_auto_schema(
        operation_summary="The Get vendor API, Retrive the data for Vendor by vendor_id",
        manual_parameters=[
            
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),        ],
        
        responses={
            200: "Data found Successfully",
            500: "Internal server error",
        }
    )
    def get(self,request,vendor_id):
        try:
            if vendor_id is not None:
                vendorDetails = Vendor.objects.get(id=vendor_id)
                seralizer = vendorDeatailsSeralizer(vendorDetails) 
                return Response({'status': status.HTTP_200_OK, 'data': seralizer.data, 'responseMessage': 'Data found Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,  'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
            operation_summary="The Update Vendor API, Update the Vendor profile ",
        manual_parameters=[
            
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),

        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING,default=None),
                'contact_details': openapi.Schema(type=openapi.TYPE_STRING,default=None),
                'address': openapi.Schema(type=openapi.TYPE_STRING,default=None),
                'vendor_code': openapi.Schema(type=openapi.TYPE_STRING,default=None)
            },
            required=['name', 'contact_details', 'address', 'vendor_code'],
        )
        
    )
    def put(self,request, vendor_id):
        try:
            data = request.data
            vendorDetails = Vendor.objects.get(id=vendor_id)
            seralizer = vendorSerailzer(vendorDetails,data=data,partial= True)
            if seralizer.is_valid():
                seralizer.save()
                return Response({'status': status.HTTP_200_OK, 'data': seralizer.data, 'responseMessage': 'Data updated Successfully'}, status=status.HTTP_200_OK)
            return Response({'status':status.HTTP_400_BAD_REQUEST,  'responseMessage': seralizer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,  'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_summary="The delete Vendor API, Delete the Vendor by vendor_id",
        manual_parameters=[
            
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ],
        
        responses={
            200: "vendor deleted Successfully",
            500: "Internal server error",
        }
    )
    def delete(self,request,vendor_id):
        try:
            vendorDetails = Vendor.objects.get(id=vendor_id)
            vendorDetails.delete()
            return Response({'status': status.HTTP_200_OK, 'responseMessage': 'vendor deleted Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,  'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    


# ========================================= Purchase Order ============================================



class GetCreatePurchaseOrder(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            operation_summary="Create a purchase order API, create a purchase order and assign it to the vendor",
            type=openapi.TYPE_OBJECT,
            properties={
                'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
                'delivery_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                ))
            }
        ),
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ]
    )
    def post(self,request):
        try:
            data  = request.data
            seralizer = PurchaseOrderSeralizer(data=data)
            if seralizer.is_valid():
                seralizer.save()
                return Response({'status': status.HTTP_201_CREATED, 'data': seralizer.data, 'responseMessage': 'Purches order created successfully'}, status=status.HTTP_201_CREATED)
            return Response({'status':status.HTTP_400_BAD_REQUEST,  'responseMessage': seralizer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,  'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @swagger_auto_schema(
        operation_summary="GET purches order API , provide the list of all purches order ",
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ],
        responses={
            200: "Data found Successfully",
            500: "Internal server error",
        }
    )
    def get(self,request):
        try :
            orderDetails = PurchaseOrder.objects.all()
            seralizer = PurchaseOrderDetailsSeralizer(orderDetails, many = True)
            return Response({'status': status.HTTP_200_OK, 'data': seralizer.data, 'responseMessage': 'Data found successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,  'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PurchesOrderDetails(APIView):
    @swagger_auto_schema(
        operation_summary="Get Purches order API, get the purches order details by po_id  ",
        operation_description="",
        manual_parameters=[
            openapi.Parameter('po_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='po_id is id of Purches order'),
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ],
        responses={
            200: "Data found Successfully",
            500: "Internal server error",
        }
    )
    def get(self,request,po_id):
        try:
            print(po_id)
            po_details = PurchaseOrder.objects.get(id = po_id)
            seralizer = PurchaseOrderDetailsSeralizer(po_details)
            return Response({'status': status.HTTP_200_OK, 'data': seralizer.data, 'responseMessage': 'Data found successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,  'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_summary="Update purches order API update the Purches Order",
        operation_description="Only pass those parameters those you have to update remaining  parametes remove ",
        manual_parameters=[
            openapi.Parameter('po_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='po_id is id of Purches order'),
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'vendor': openapi.Schema(type=openapi.TYPE_INTEGER,default=1),
            'delivery_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                    'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )),
            'status':openapi.Schema(type=openapi.TYPE_STRING,enum=['pending','completed','canceled']),
            'acknowledgment_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            'quality_rating': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT)
        }
        
    ))
    def put(self, request, po_id):
        # try:
            po_details = PurchaseOrder.objects.get(id=po_id)
            serializer = PurchaseOrderDetailsSeralizer(po_details, data=request.data, partial=True)
            statuss = request.data.get('status', None)
            if statuss is not None and statuss == 'completed':
                quality_rating = request.data.get('quality_rating', None)
                if quality_rating is None:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'responseMessage': 'Please provide the quality rating'}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'data': serializer.data, 'responseMessage': 'Data updated Successfully'}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'responseMessage': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'responseMessage': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="The delete purches order api , delete the purches order ",
        manual_parameters=[
            openapi.Parameter('po_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='po_id is id of purches oreder'),
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ],
        
        responses={
            200: "Purches order deleted Successfully",
            500: "Internal server error",
        }
    )
    def delete(self,request,po_id):
        try: 
            po_details = PurchaseOrder.objects.get(id=po_id)
            po_details.delete()
            return Response({'status': status.HTTP_200_OK, 'responseMessage': 'Purches order deleted Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        






# ================================= Vender Historical performace ===============================================




class VendorPerformance(APIView):
    @swagger_auto_schema(
        operation_summary="The Vendor performace list of Vendor performace and analysis ",
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='vendor_id is the id of vendor'),
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authentication Token', default='Bearer ', type=openapi.TYPE_STRING),
        ],
        responses={
            200: "Data found Successfully",
            500: "Internal server error",
        },
        tags=['Vender Performance']
    )
    def get(self, request, vendor_id):
        try:
            performace = HistoricalPerformance.objects.filter(vendor = vendor_id)
            
            serializer = HistoricalPerformanceSeralizer(performace, many = True)
            return Response({'status': status.HTTP_200_OK, 'data': serializer.data, 'responseMessage': 'Data found successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# ============================ User Flow =========================
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    '''
    This is JWT token genration function 
    
    '''
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class Register(APIView):
    @swagger_auto_schema(
        operation_summary="The User Registration API",
        operation_description="The User Registration API take a username , email ,password paramertes to create a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL), 
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                # Add other properties as needed
            },
            required=['username','email', 'password']  
        ),
        
        tags= ['User']
    )
    def post(self,request):
        try:
            data = request.data
            
            if User.objects.filter(email=data['email']).exists():
                return Response({'status': status.HTTP_400_BAD_REQUEST,'responseMessage':'Email addres alreeady exists'}, status=status.HTTP_400_BAD_REQUEST)
            User.objects.create(username = data['username'],email= data['email'],password= data['password']).save()

            return Response({'status': status.HTTP_201_CREATED,'responseMessage': 'Registration successfull'}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Login(APIView):
    @swagger_auto_schema(
        operation_description="The user login api take a email and password for the user authentication and login",
        operation_summary="The User login API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL), 
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                
            },
            required=['email', 'password']  
        ),
        responses={
            200: openapi.Response('Logged in successfully'),  
            400: openapi.Response('User not found'), 
            500: openapi.Response('Internal Server Error'),  
        },
        tags= ['User']
    )
    def post(self,request):
        try:
            data = request.data
            user = User.objects.get(email = data['email'])
            print(user.password)
            if user is not None:
                if user.password == data['password']:

                    login(request,user)
                    token = get_tokens_for_user(user)
                    return Response({'status': status.HTTP_200_OK, 'token': token['access'], 'responseMessage': 'Logged in successfully'}, status=status.HTTP_200_OK)
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'responseMessage': 'Password not match'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'responseMessage': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'responseMessage': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




           
