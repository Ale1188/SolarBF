from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='orders'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('update_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]