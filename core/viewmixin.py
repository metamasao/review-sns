from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import UserPassesTestMixin


class CustomUserPassTestMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class NavPageMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if getattr(self, 'nav_page', None):
            context['nav_page'] = self.nav_page
        return context


class AjaxPostRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        ajax_request = request.headers.get('x-requested-with')
        if ajax_request != 'XMLHttpRequest' or request.method != 'POST':
            return HttpResponseBadRequest()
        return super().dispatch(request, *args, **kwargs)


class AuthorMixin:

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)