from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self):
        from django.db.models.signals import post_save,pre_save
        from main import signals
        from main import models
        pre_save.connect(signals.historical_performance,sender=models.PurchaseOrder)
        post_save.connect(signals.create_profile, sender=models.Vendor)
        post_save.connect(signals.update_details , sender=models.PurchaseOrder)

