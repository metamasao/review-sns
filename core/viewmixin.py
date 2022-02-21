from django.http import HttpResponseBadRequest


class PageMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if getattr(self, 'page', None):
            context['page'] = self.page
        return context


class AjaxPostRequired:

    def dispatch(self, request, *args, **kwargs):
        ajax_request = request.headers.get('x-requested-with')
        if ajax_request != 'XMLHttpRequest' or request.method != 'POST':
            return HttpResponseBadRequest()
        return super().dispatch(request, *args, **kwargs)