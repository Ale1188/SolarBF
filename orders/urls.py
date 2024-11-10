from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='orders'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('order/<int:order_id>/order_completed/', views.toggle_order_completed, name='toggle_order_completed'),

]