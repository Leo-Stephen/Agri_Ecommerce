from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('my_products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


@login_required
def my_products(request):
    products = Product.objects.filter(farmer=request.user).order_by('-created_at')
    return render(request, 'my_products.html', {'products': products})


@login_required
def sort_products(request):
    sort_by = request.GET.get('sort', 'newest')

    # Get products for the current user
    products = Product.objects.filter(farmer=request.user)

    # Apply sorting based on selection
    if sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    elif sort_by == 'price-high':
        products = products.order_by('-price')
    elif sort_by == 'price-low':
        products = products.order_by('price')

    # Render only the products grid portion
    html = render_to_string('product_grid_partial.html', {
        'products': products
    }, request=request)

    return HttpResponse(html)


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if 'image' in request.FILES:
                if product.image:
                    try:
                        product.image.delete(save=False)
                    except:
                        pass
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product_page.html', {
        'form': form,
        'product': product
    })


@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, farmer=request.user)
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('my_products')
    return redirect('my_products')


@login_required
def toggle_featured(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, farmer=request.user)
        product.is_featured = not product.is_featured
        product.save()
        messages.success(request, f'Product {"featured" if product.is_featured else "unfeatured"} successfully!')
    return redirect('my_products')


def customer_dashboard(request):
    featured_products = Product.objects.filter(is_featured=True).order_by('-created_at')[:6]
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'customer_app/customer_dashboard.html', context)
