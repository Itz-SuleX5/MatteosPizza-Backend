from django.urls import path
from . import views

urlpatterns = [
    # Ingredientes
    path('ingredients/create/', views.create_ingrediente, name='create_ingrediente'),
    path('ingredients/', views.list_ingredientes, name='list_ingredientes'),
    path('ingredients/<int:pk>/', views.get_ingrediente, name='get_ingrediente'),
    path('ingredients/<int:pk>/update/', views.update_ingrediente, name='update_ingrediente'),
    path('ingredients/<int:pk>/delete/', views.delete_ingrediente, name='delete_ingrediente'),
    
    # Productos
    path('api/create/', views.create_product, name='create_product'),
    path('api/', views.list_products, name='list_products'),
    path('api/<int:pk>/', views.get_product, name='get_product'),
    path('api/<int:pk>/update/', views.update_product, name='update_product'),
    path('api/<int:pk>/delete/', views.delete_product, name='delete_product'),
]