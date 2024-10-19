# from django.db import models
# from django.contrib.auth.models import User
# from decimal import Decimal
# from products.models import Product, Coupon
# from cart.models import CartItem
# from django.utils import timezone

# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('paid', 'Paid'),
#         ('shipped', 'Shipped'),
#         ('completed', 'Completed'),
#         ('canceled', 'Canceled'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart_items = models.ManyToManyField(CartItem)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
#     final_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     paid_at = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f'Order {self.id} by {self.user.username}'

#     def mark_as_paid(self):
#         self.status = 'paid'
#         self.paid_at = timezone.now()
#         self.save()

# class Payment(models.Model):
#     PAYMENT_METHOD_CHOICES = (
#         ('credit_card', 'Credit Card'),
#         ('paypal', 'PayPal'),
#         ('bank_transfer', 'Bank Transfer'),
#     )

#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     paid_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Payment for Order {self.order.id} via {self.payment_method}'
