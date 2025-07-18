from django.urls import path
from .views import (
    create_order,
    list_orders,
    my_orders,
    get_order,
    update_order_status,
    delete_order,
)

urlpatterns = [
    path('api/create/', create_order, name='create-order'),
    path('api/', list_orders, name='list-orders'),
    path('api/my-orders/', my_orders, name='my-orders'),
    path('api/<int:pk>/', get_order, name='get-order'),
    path('api/<int:pk>/update-status/', update_order_status, name='update-status'),
    path('api/<int:pk>/delete/', delete_order, name='delete-order'),
]
