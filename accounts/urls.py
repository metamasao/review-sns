from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

from .views import SignupView, UserUpdateView, UserFollowView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('<uuid:pk>/update/', UserUpdateView.as_view(), name="update"),
    path('follow/', UserFollowView.as_view(), name='follow'),
    # path('follow/', )
    # path('user-detail/')
]