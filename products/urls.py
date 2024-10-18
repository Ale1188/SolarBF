from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.productView, name='products'),
    path('management/', views.management, name='management'),
    path('categories/', views.category_list, name='categories'),
    path('products/add/', views.add_product, name='add_product'),
    path('categories/add/', views.add_category, name='add_category'),
    path('products/list', views.product_list, name='product_list'),
    path('categories/edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('products/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]