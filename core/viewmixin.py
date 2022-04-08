"""
DRYやThinViewの設計思想に基づいてこのモジュールを作成しました。
各アプリで使用される汎用性の高いView Mix-inのクラスを定義しています。
"""

from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin


class CustomUserPassTestMixin(UserPassesTestMixin):
    """
    モデルの著者とリクエストしたユーザーが異なる場合に403を返します。
    """
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class SearchResultMixin:
    """
    検索用のMix-inクラスです。ListViewなどで継承して使用してください。
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)|Q(author__icontains=query)
            )
        return queryset 


class NavPageMixin:
    """
    リクエストに応じてNavBarで該当LinkをactiveにするためのMix-inです。
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if getattr(self, 'nav_page', None):
            context['nav_page'] = self.nav_page
        return context


class AjaxPostRequiredMixin:
    """
    非同期通信(ajax)用のMix-inです。
    """
    def dispatch(self, request, *args, **kwargs):
        """
        リクエストが非同期通信でない、またはリクエストメソッドがPostでなければ400を返します。
        """
        ajax_request = request.headers.get('x-requested-with')
        if ajax_request != 'XMLHttpRequest' or request.method != 'POST':
            return HttpResponseBadRequest()
        return super().dispatch(request, *args, **kwargs)


class AuthorMixin:
    """
    モデルの著者とリクエストユーザーを紐づけます。
    views.CreateViewなどで使用してください。
    """
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)