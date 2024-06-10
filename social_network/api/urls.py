from django.urls import path
from .views import register, login, search_users, send_friend_request, respond_friend_request, list_friends, pending_requests

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('search/', search_users, name='search_users'),
    path('friend-request/send/', send_friend_request, name='send_friend_request'),
    path('friend-request/respond/<int:pk>/', respond_friend_request, name='respond_friend_request'),
    path('friends/', list_friends, name='list_friends'),
    path('friend-requests/pending/', pending_requests, name='pending_requests'),
]
