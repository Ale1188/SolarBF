from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_view, name='products'),
    path('management/', views.management, name='management'),
    path('categories/', views.category_list, name='categories'),
    path('add/', views.add_product, name='add_product'),
    path('categories/add/', views.add_category, name='add_category'),
    path('list', views.product_list, name='product_list'),
    path('categories/edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('list/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('list/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('coupons/', views.coupon_list, name='coupon'),
    path('coupons/create/', views.create_coupon, name='create_coupon'),
    path('coupons/edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('coupons/delete_coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
    path('coupon/<int:coupon_id>/', views.coupon_detail, name='coupon_detail'),
]