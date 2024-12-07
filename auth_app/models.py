from django.db import models
from django.contrib.auth.models import User
from order_app.models import Order  # Import Order model

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, default='farmer')

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, default='customer')

    @property
    def order_count(self):
        from order_app.models import Order
        return Order.objects.filter(user=self.user).count()
