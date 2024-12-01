# from django.db import models
# from django.contrib.auth.models import User
# from product_app.models import Product

# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('PENDING', 'Pending'),
#         ('PROCESSING', 'Processing'),
#         ('SHIPPED', 'Shipped'),
#         ('DELIVERED', 'Delivered'),
#         ('CANCELLED', 'Cancelled'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Order #{self.id} by {self.user.username}"
    
from django.db import models
from django.contrib.auth.models import User
from product_app.models import Product  # Import the Product model

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=100, unique=True, primary_key=True, default='unknown_order_id')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Paid, Cancelled
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"  # Assuming Product model has a 'name' field