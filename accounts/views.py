from django.views import generic
from .forms import CustomUserCreationForm

class SingupView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'


class UserDetail(generic.TemplateView):
    template_name='accounts/user_detail.html'
