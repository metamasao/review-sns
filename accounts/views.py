import logging
from django.views import generic
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .forms import CustomUserCreationForm
from .models import CustomUser, Follow
from core.viewmixin import AjaxPostRequiredMixin

logger = logging.getLogger(__name__)


class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    login_url = 'accounts:login'


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    fields = ('username', 'email', 'profile')
    template_name = 'accounts/user_update.html'
    login_url = 'accounts:login'


class UserFollowView(AjaxPostRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('id')
        action = request.POST.get('action')
        logger.debug(user_id)
        logger.debug(action)

        user_to = get_object_or_404(
            CustomUser,
            id=user_id
        )        
        user_from = self.request.user
        if action == 'follow':
            Follow.objects.create_follow(
                user_from=user_from,
                user_to=user_to
            )
        else:
            Follow.objects.filter(
                user_from=user_from,
                user_to=user_to
            ).delete()

        return JsonResponse({'status': 'ok'})
