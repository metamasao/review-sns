from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

from .views import SingupView, UserDetail, UserUpdate

app_name = 'accounts'
urlpatterns = [
    path('signup/', SingupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('/<uuid:pk>/', UserDetail.as_view(), name='detail'),
    path('/<uuid:pk>/update/', UserUpdate.as_view(), name="user_update"),
    # path('follow/', )
    # path('user-detail/')
]