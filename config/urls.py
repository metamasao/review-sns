from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # adminへのリクエストはdjango-admin-honeypotなどで対応可能
    path('kessiteadmindehagozaimasen/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('review/', include('review.urls')),
    path('', include('books.urls')),
]
