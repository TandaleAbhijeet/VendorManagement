from django.db import models
import uuid
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(blank=True,null= True)
    quality_rating_avg = models.FloatField(blank=True,null= True)
    average_response_time = models.FloatField(blank=True,null= True)
    fulfillment_rate = models.FloatField(blank=True,null= True)

    def __str__(self):
        return self.name
    


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True, default= uuid.uuid4)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    
    def save(self, *args, **kwargs):
        if self.items:
            total_quantity = sum(item.get('quantity',0) for item in self.items)
            self.quantity = total_quantity
        if self.vendor:
            print('we are in the model')
            if not self.issue_date:
                self.issue_date = timezone.now()
        if not self.status:
            self.status = 'pending' 
        super().save( *args, **kwargs)
    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
    

