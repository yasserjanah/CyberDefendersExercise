
from django.urls import path
from dockerApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', views.LoginUser, name='login'),
    path('accounts/register', views.RegisterUser, name='register'),
    path('accounts/logout', views.LogoutUser, name='logout'),
    path('accounts/info', views.GetUserInfo, name='get_user_info'),
    path('instances/create', views.LaunchContainer, name='create_container'),
    path('instances/status', views.GetTaskStatus, name='get_status'),
    path('instances/images', views.GetAvailableImages, name='get_images'),
    path('instances/remove', views.RemoveContainer, name='remove_container'),
    path('instances', views.GetUserInstances, name='get_user_instances'),
]
