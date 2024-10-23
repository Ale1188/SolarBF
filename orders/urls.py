from django.urls import path
from . import views

urlpatterns = [
    path('', views.productView, name='orders'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
]