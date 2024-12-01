import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Order, OrderItem
from customer_app.models import CartItem  # Assuming Cart is in customer_app
from django.contrib.auth.decorators import login_required

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def initiate_payment(request):
    if request.method == 'POST':
        # Fetch cart items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items:
            return redirect('customer_app:cart')  # Redirect to cart page if empty

        # Calculate total cart amount
        cart_total = sum(item.total_price for item in cart_items)

        # Calculate the amount in paise (1 INR = 100 paise)
        amount_in_paise = int(cart_total * 100)

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': '1'
        })

        # Create Order and OrderItems
        order = Order.objects.create(
            user=request.user,
            order_id=razorpay_order['id'],
            amount=cart_total
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,  # Assuming `item.product` is a Product object
                quantity=item.quantity,
                price=item.product.price
            )

        context = {
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'order_id': razorpay_order['id'],
            'amount': amount_in_paise,  # Pass the calculated amount in paise
            'order': order,
        }
        return render(request, 'order_app/payment.html', context)

    return redirect('customer_app:cart')  # Redirect to cart page if empty

@login_required
def payment_callback(request):
    if request.method == 'POST':
        payment_data = request.POST
        razorpay_payment_id = payment_data.get('razorpay_payment_id')
        razorpay_order_id = payment_data.get('razorpay_order_id')

        try:
            # Update order status
            order = Order.objects.get(order_id=razorpay_order_id)
            order.payment_id = razorpay_payment_id
            order.status = 'Paid'
            order.save()

            # Clear the cart
            CartItem.objects.filter(user=request.user).delete()  # Clear CartItems for the user

            return redirect('order_success')  # Redirect to order success page
        except Exception as e:
            print(f"Error during payment callback: {e}")
            return redirect('order_failed')  # Redirect to order failure page

    return redirect('customer_app:cart')  # Redirect to home for invalid requests

# order_app/views.py
@login_required
def order_success(request):
    return render(request, 'order_app/order_success.html')

@login_required
def order_failed(request):
    return render(request, 'order_app/order_failed.html')