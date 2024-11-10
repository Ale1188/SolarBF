from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from accounts.views import is_admin, is_staff
from django.views.decorators.http import require_POST


@user_passes_test(is_staff)
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    
    return render(request, 'admin/orders.html', {
        'orders': orders,
    })

@user_passes_test(is_staff)
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect('orders')

    return render(request, 'orders/delete_confirmation.html', {'order': order})

@user_passes_test(is_staff)
@require_POST
def toggle_order_completed(request, order_id):
    order = Order.objects.get(id=order_id)
    order.is_completed = not order.is_completed
    order.save()
    return redirect('orders')