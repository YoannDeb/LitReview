from django.urls import path

from . import views

app_name = 'reviews'
urlpatterns = [
    path('', views.index, name='index'),
    path('user_follows/', views.user_follows, name='user_follows')
]
