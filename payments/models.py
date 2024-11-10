from django.conf import settings
from django.db import models
from decimal import Decimal
from products.models import Coupon
from cart.models import CartItem
from django.utils import timezone
from config.constants import STATUS_CHOICES

class PaymentOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_in_orders')
    cart_items = models.ManyToManyField(CartItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    street_address = models.CharField(max_length=255, default='Unknown')
    city = models.CharField(max_length=100, default='Unknown')
    state = models.CharField(max_length=100, default='Unknown')
    zip_code = models.CharField(max_length=20, default='Unknown')
    country = models.CharField(max_length=100, default='Unknown')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
    def mark_as_paid(self):
        if self.coupon and self.coupon.uses < self.coupon.max_uses:
            self.coupon.uses += 1
            self.coupon.save()
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('debit', 'Debit'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    )

    order = models.ForeignKey(PaymentOrder, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for Order {self.order.id} via {self.payment_method}'