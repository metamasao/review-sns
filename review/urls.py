from django.urls import path
from .views import (
    ReviewListView,
    ReviewAuthorDetailView, 
    ReviewBookDetailView,
    ReviewCreateView, 
    ReviewDetailView, 
    ReviewUpdateView, 
    ReviewDeleteView, 
    LikeView
    )

app_name = 'review'
urlpatterns = [
    path('<uuid:pk>/author-detail/', ReviewAuthorDetailView.as_view(), name='author-detail'),
    path('<uuid:pk>/book-detail/', ReviewBookDetailView.as_view(), name='book-detail'),
    path('<uuid:pk>/create/', ReviewCreateView.as_view(), name='create'),
    path('<uuid:pk>/detail/', ReviewDetailView.as_view(), name='detail'),
    path('<uuid:pk>/update/', ReviewUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', ReviewDeleteView.as_view(), name='delete'),
    path('like/', LikeView.as_view(), name='like'),
    path('', ReviewListView.as_view(), name='list'),
]