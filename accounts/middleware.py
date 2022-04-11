from django.http import HttpResponseForbidden
from django.urls import reverse


class DenyAccesstoAdminMiddleware:
    """
    superuser以外のユーザーがadminにリクエストした時に、
    viewを呼び出す前に403のレスポンスを返します。
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        admin_path = reverse('admin:index')
        if request.path.startswith(admin_path) and not request.user.is_superuser:
            return HttpResponseForbidden()
        return None
