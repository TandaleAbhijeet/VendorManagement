from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth.models import User
from django.utils import timezone
class vendorSerailzer(ModelSerializer):
    
    class Meta:
        model = Vendor
        exclude = ['on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']

    def update(self, instance, validated_data):
        new_validate_data ={}
        for key, value in validated_data.items():
            if 'string' not in  value:
               new_validate_data[key] = value
        print('final dict:', new_validate_data)
        return super().update(instance, new_validate_data)
    
class vendorDeatailsSeralizer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSeralizer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['vendor','delivery_date','items']


class PurchaseOrderDetailsSeralizer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    
    def update(self, instance, validated_data):
        new_validated_data = {}
        po_details = PurchaseOrder.objects.get(pk=instance.pk)
        for key ,value in validated_data.items():
            if value is 'string':
                continue
            if key == 'quality_rating' and value == 0:
                continue
            if key == 'vendor':
                if value == po_details.vendor:
                    print('we are in the same vendor')
                    continue
                else:
                    new_validated_data['issue_date'] = timezone.now()

            if key == 'items':
                if value == []:
                    raise ValueError('Need a items in purches order')
                else:
                    quantity = 0
                    for val in value:
                        quantity = quantity+val['quantity']
                        new_validated_data['quantity']= quantity
            if key == 'status':
                if value == 'completed':
                    new_validated_data['acknowledgment_date'] = timezone.now()
            new_validated_data[key]= value

        return super().update(instance, new_validated_data)

        
class HistoricalPerformanceSeralizer(ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'






