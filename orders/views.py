from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def productView(request):
    orders = Order.objects.all()
    
    return render(request, 'admin/orders.html', {
        'orders': orders,
    })
