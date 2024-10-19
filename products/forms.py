from django import forms
from .models import Product, Category, Coupon

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category")

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'max_uses']