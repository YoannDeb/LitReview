from django.urls import path, include

from . import views

app_name = 'reviews'
urlpatterns = [
    path('', views.index, name='index'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('ticket_creation/', views.ticket_creation, name='ticket_creation'),
    path('ticket_response/', views.ticket_response, name='ticket_response'),
    path('review_creation/', views.review_creation, name='review_creation'),
    path('user_follows/', views.user_follows, name='user_follows'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.user_creation, name='signup'),
    path('delete_ticket/<int:pk>', views.TicketDeleteView.as_view(), name='delete_ticket'),
    path('delete_review/<int:pk>', views.ReviewDeleteView.as_view(), name='delete_review'),
    path('delete_follow/<int:pk>', views.UserFollowDeleteView.as_view(), name='delete_follow'),
]
