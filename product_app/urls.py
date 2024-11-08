# product_app/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import add_product, my_products, sort_products, edit_product, delete_product, toggle_featured

urlpatterns = [
    path('add_product/', add_product, name='add_product'),  # URL for adding a product
    path('my_products/', my_products, name='my_products'),  # URL for viewing the user's products
    path('sort_products/', sort_products, name='sort_products'),  # URL for sorting products
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('toggle-featured/<int:product_id>/', toggle_featured, name='toggle_featured'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
