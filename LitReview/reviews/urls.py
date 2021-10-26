from django.urls import path

from . import views

app_name = 'reviews'
urlpatterns = [
    path('', views.index, name='index'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('user_follows/', views.user_follows, name='user_follows'),
]
