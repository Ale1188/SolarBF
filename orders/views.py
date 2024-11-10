from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.views import is_admin, is_staff
from config.constants import STATUS_CHOICES
from django.views.decorators.http import require_POST



@user_passes_test(is_staff)
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'admin/orders.html', {
        'orders': orders,
        'status_choices': STATUS_CHOICES,
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

@require_POST
@login_required
@user_passes_test(is_staff)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, "Order status updated successfully!")
    else:
        messages.error(request, "Invalid status selected.")

    return redirect('orders')