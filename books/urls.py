from django.urls import path

from .views import BookListHomeView, BookCreateView

app_name = 'books'
urlpatterns = [
    path('<uuid:pk>/', BookListHomeView.as_view(), name='home'),
    path('create/', BookCreateView.as_view(), name='create'),
    # path('search/', BookSearchResultView.as_view(), name='search_result'),
    path('', BookListHomeView.as_view(), name='home'),
]
