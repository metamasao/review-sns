from django.urls import path

from .views import BookListHomeView, BookDetailView, BookCreateView

app_name = 'books'
urlpatterns = [
    path('<uuid:pk>/detail/', BookDetailView.as_view(), name='detail'),
    path('<uuid:pk>/', BookListHomeView.as_view(), name='home'),
    path('create/', BookCreateView.as_view(), name='create'),
    path('', BookListHomeView.as_view(), name='home'),
]
