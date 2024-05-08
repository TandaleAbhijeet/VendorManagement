"""
URL configuration for venderManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import *

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Vendor API",
        default_version='v1',
        description="APIs to manage vendors",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # ============ Vender Urls ================
    path('api/vendors/',GetCreatevendor.as_view()),
    path('api/vendors/<int:vendor_id>',VendorOpration.as_view()),

    # =============== PurchesOrder Urls =============
    path('api/purchase_orders/',GetCreatePurchaseOrder.as_view()),
    path('api/purchase_orders/<int:po_id>/',PurchesOrderDetails.as_view()),

    # =============== Vender performance  Urls  ===========
    path('api/vendors/<int:vendor_id>/performance',VendorPerformance.as_view()),
    # ================ User Urls ==========
    path('Register/',Register.as_view()),
    path('login/',Login.as_view())


]

