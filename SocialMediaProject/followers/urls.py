from django.urls import path
from . import views

app_name = 'followers'

urlpatterns = [
    path('<str:username>/toggle/', views.toggle_follow_view, name='toggle_follow'),
    path('<str:username>/followers/', views.followers_list_view, name='followers_list'),
    path('<str:username>/following/', views.following_list_view, name='following_list'),
]
