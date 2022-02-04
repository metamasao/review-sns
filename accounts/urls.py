from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

from .views import SingupView, UserDetail

urlpatterns = [
    path('signup/', SingupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('<username>/<uuid:pk>/', UserDetail.as_view(), name='detail'),
    # path('follow/', )
    # path('user-detail/')
]