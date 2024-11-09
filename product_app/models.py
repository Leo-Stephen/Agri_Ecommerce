from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.templatetags.static import static


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains'),
        ('dairy', 'Dairy'),
        ('tools', 'Tools & Equipment'),
        ('seeds', 'Seeds & Saplings'),
        ('pesticides', 'Pesticides & Fertilizers'),
        ('organic', 'Organic Products'),
        ('livestock', 'Livestock & Feed'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return static('images/default_product.jpg')
