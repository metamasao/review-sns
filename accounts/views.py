from django.views import generic
from django.contrib.auth import login

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class SingupView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

class UserDetail(generic.DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'


class UserUpdate(generic.UpdateView):
    model = CustomUser
    fields = ('username', 'email', 'profile')
    template_name = 'accounts/user_update.html'