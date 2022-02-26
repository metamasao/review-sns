from django.urls import path
from .views import CreateReview

app_name = 'review'
urlpatterns = [
    path('<uuid:pk>/create/', CreateReview.as_view(), name='create'),
]