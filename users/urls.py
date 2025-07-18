from django.urls import path
from . import views

urlpatterns = [
    path('profile/create/', views.create_user_profile, name='create_user_profile'),
    path('api/', views.list_users, name='list_users'),
    path('profile/<str:auth0_id>/', views.get_user_profile, name='get_user_profile'),
    path('profile/', views.create_or_update_profile, name='create_or_update_profile'),
]