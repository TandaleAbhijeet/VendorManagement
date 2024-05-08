from django.db.models.signals import post_save ,pre_save
from django.dispatch import receiver
from .models import *
from django.utils import timezone
@receiver(post_save, sender=Vendor) 
def create_profile(sender, instance, created, **kwargs):
    print('we are in singals')
    if created:
        print("we are in created" )
        print('instance.fulfillment_rate',instance.fulfillment_rate)
        if (not instance.on_time_delivery_rate  and not instance.quality_rating_avg  and not  instance.average_response_time  and not  instance.fulfillment_rate ):
            instance.on_time_delivery_rate = 0
            instance.quality_rating_avg = 0
            instance.average_response_time = 0
            instance.fulfillment_rate = 0
            instance.save()

@receiver(post_save, sender = PurchaseOrder)
def update_details(sender, instance, created, **kwargs):
        vendor_user = instance.vendor
        print(instance.status)
        if instance.status == 'completed':
            vendor_user.on_time_delivery_rate = on_time_delivery_rate_avg_calculation(vendor_user)
            vendor_user.quality_rating_avg = quality_rating_avg_calculation(vendor_user)
            vendor_user.average_response_time = average_response_time_calculation(vendor_user)
            vendor_user.fulfillment_rate = fulfillment_rate_calculation(vendor_user)
            vendor_user.save()



def on_time_delivery_rate_avg_calculation(vendor_user):
    completed_orders= PurchaseOrder.objects.filter(vendor = vendor_user , status = 'completed')
    completed_orders_count = completed_orders.count()
    if completed_orders_count > 0:
        on_time_delivery =0
        for order in completed_orders:
            if order.acknowledgment_date <= order.delivery_date:
                on_time_delivery+= 1
        print('delivery_rate',on_time_delivery/completed_orders_count)
        return on_time_delivery/completed_orders_count
    return 0

    

def quality_rating_avg_calculation(vendor_user):
    completed_orders= PurchaseOrder.objects.filter(vendor = vendor_user , status = 'completed').exclude(quality_rating= None)
    completed_orders_count = completed_orders.count()
    quality_ratirng = 0
    if completed_orders_count> 0:
       total_rating = sum( order.quality_rating for order in completed_orders)
       print('avg rating',total_rating/completed_orders_count    )
       return total_rating/completed_orders_count    
    return 0

def average_response_time_calculation(vendor_user):
    completed_orders= PurchaseOrder.objects.filter(vendor = vendor_user).exclude(acknowledgment_date = None)
    completed_orders_count = completed_orders.count()
    if completed_orders_count>0:
        total_response_time = sum((order.acknowledgment_date- order.issue_date).total_seconds() for order in completed_orders)
        
        print('response time ',total_response_time/completed_orders_count )
        return round((total_response_time/completed_orders_count )/60,2)


def fulfillment_rate_calculation(vendor_user):
    total_order = PurchaseOrder.objects.filter(vendor = vendor_user)
    completed_oreder = total_order.filter(status = 'completed').count()
    if completed_oreder>0: 
        print('fullfill mant rate',completed_oreder/total_order.count())
        return completed_oreder/total_order.count()
    return 0





@receiver(pre_save , sender= PurchaseOrder)
def historical_performance(sender, instance, **kwargs):
    Vendor_user = instance.vendor
    if instance.status == 'completed':
            update_historcial_performance(Vendor_user,Vendor_user.on_time_delivery_rate,Vendor_user.quality_rating_avg,Vendor_user.average_response_time,Vendor_user.fulfillment_rate)


       
def update_historcial_performance(vendor,on_time_delivery_rate,quality_rating_avg,average_response_time,fulfillment_rate):
    HistoricalPerformance.objects.create(vendor=vendor,
                                         date = timezone.now(),
                                        on_time_delivery_rate=on_time_delivery_rate,
                                        quality_rating_avg=quality_rating_avg,
                                        average_response_time=average_response_time,
                                        fulfillment_rate=fulfillment_rate).save()
    
