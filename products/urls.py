from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/', views.category_list, name='categories'),
    path('management/', views.management, name='management'),
]