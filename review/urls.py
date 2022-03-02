from django.urls import path
from .views import ReviewCreateView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView, LikeView

app_name = 'review'
urlpatterns = [
    path('<uuid:pk>/create/', ReviewCreateView.as_view(), name='create'),
    path('<uuid:pk>/detail/', ReviewDetailView.as_view(), name='detail'),
    path('<uuid:pk>/update/', ReviewUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', ReviewDeleteView.as_view(), name='delete'),
    path('like/', LikeView.as_view(), name='like'),
]