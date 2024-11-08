from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from auth_app.models import FarmerProfile, CustomerProfile
from product_app.models import Product
from customer_app.models import CartItem  # Use CartItem instead of an Order model

# Custom check to ensure only superusers can access the admin dashboard
def admin_check(user):
    return user.is_superuser

# Ensure the user is logged in and passes the admin check
@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
    # Count the number of farmers, customers, products, and cart items
    farmer_count = FarmerProfile.objects.count()
    customer_count = CustomerProfile.objects.count()
    product_count = Product.objects.count()
    cart_item_count = CartItem.objects.count()  # Count CartItem entries as a substitute for orders

    context = {
        'farmer_count': farmer_count,
        'customer_count': customer_count,
        'product_count': product_count,
        'cart_item_count': cart_item_count,
    }

    # Render the admin dashboard template
    return render(request, 'admin_app/admin_dashboard.html', context)


# View to list all farmers
@login_required
@user_passes_test(admin_check)
def farmer_list(request):
    farmers = FarmerProfile.objects.all()  # Get all farmers
    context = {
        'farmers': farmers,
    }
    return render(request, 'admin_app/farmer_list.html', context)


# View to list all customers
@login_required
@user_passes_test(admin_check)
def customer_list(request):
    customers = CustomerProfile.objects.all()  # Get all customers
    context = {
        'customers': customers,
    }
    return render(request, 'admin_app/customer_list.html', context)


# View to list all products
@login_required
@user_passes_test(admin_check)
def product_list(request):
    products = Product.objects.all()  # Get all products
    context = {
        'products': products,
    }
    return render(request, 'admin_app/product_list.html', context)


# View to list all cart items (as a substitute for order list)
@login_required
@user_passes_test(admin_check)
def order_list(request):
    cart_items = CartItem.objects.all()  # Get all cart items
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'admin_app/order_list.html', context)
