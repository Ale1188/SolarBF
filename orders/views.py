from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def productView(request):
    orders = Order.objects.filter(user=request.user)
    
    return render(request, 'admin/orders.html', {
        'orders': orders,
    })

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect('orders')

    return render(request, 'orders/delete_confirmation.html', {'order': order})