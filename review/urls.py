from django.urls import path
from .views import ReviewCreateView, ReviewDetailView

app_name = 'review'
urlpatterns = [
    path('<uuid:pk>/create/', ReviewCreateView.as_view(), name='create'),
    path('<uuid:pk>/detail/', ReviewDetailView.as_view(), name='detail'),
]