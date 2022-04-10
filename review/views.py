from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Action
from books.models import Book
from core.viewmixin import AuthorMixin, CustomUserPassTestMixin, AjaxPostRequiredMixin, NavPageMixin
from .models import Review, Like
from .forms import ReviewModelForm, CommentForm


class ReviewSidebarMixin:
    """
    Review.viewsでのサイドバーのコンテンツを追加するMix-in
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_reviews'] = Review.objects.order_by_the_number_of_likes()[:5]
        context['following_actions'] = Action.objects.get_following_actions(self.request.user)[:10]
        return context


class ReviewDetailMixin:
    """
    特定のインスタンスのListViewに対して使用するMix-in
    """
    detail_model = None

    def get(self, request, *args, **kwargs):
        self.detail_object = self.get_detail_object()
        return super().get(request, *args, **kwargs)

    def get_detail_object(self):
        detail_object = get_object_or_404(self.detail_model, pk=self.kwargs.get('pk'))
        return detail_object


class ReviewListView(LoginRequiredMixin, ReviewSidebarMixin, NavPageMixin, generic.ListView):
    """
    公開されたレビュー一覧のview
    """
    queryset = Review.objects.public()
    template_name = 'review/review_list.html'
    context_object_name = 'reviews'
    nav_page = 'review'
    paginate_by = 10


class ReviewAuthorDetailView(LoginRequiredMixin, ReviewDetailMixin, generic.ListView):
    """
    レビューの著者に基づくレビュー一覧のview
    """
    model = Review
    detail_model = get_user_model()
    template_name = 'review/review_author_detail.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        """
        リクエストしたユーザーがレビューの著者と同じであれば
        下書きのレビューも含めてクエリセットを返す。
        そうでなければ、公開されたクエリセットを返す。
        """
        queryset = super().get_queryset().filter(author=self.detail_object)
        if self.detail_object != self.request.user:
            queryset = queryset.filter(status='public')
        return queryset

    def get_context_data(self, *args, **kwargs):
        """
        著者の情報などを追加
        """
        context = super().get_context_data(*args, **kwargs)
        context['author'] = self.detail_object
        context['author_popular_reviews'] = Review.objects.order_by_the_number_of_likes().filter(
            author=self.detail_object
        )[:5]
        return context


class ReviewBookDetailView(LoginRequiredMixin, ReviewDetailMixin, generic.ListView):
    """
    特定の本に基づいてレビュー一覧を返すview
    """
    queryset = Review.objects.public()
    detail_model = Book
    template_name = 'review/review_book_detail.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(related_book=self.detail_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.detail_object
        context['same_category_books'] = Book.objects.get_same_category_books(instance=self.detail_object)
        return context


class ReviewCreateView(LoginRequiredMixin, ReviewSidebarMixin, AuthorMixin, generic.CreateView):
    """
    レビューを作成するview
    """
    form_class = ReviewModelForm
    template_name = 'review/review_create.html'

    def form_valid(self, form):
        """
        検証済みの入力されたデータから必要なデータを取得しインスタンスの属性に追加
        """
        next_book = get_object_or_404(Book, isbn=form.cleaned_data.get('isbn'))
        related_book = get_object_or_404(Book,pk=self.kwargs.get('pk'))
        form.instance.related_book = related_book
        form.instance.next_book = next_book
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, CustomUserPassTestMixin, ReviewSidebarMixin, generic.UpdateView):
    """
    レビューの更新view
    """
    model = Review
    fields = ('title', 'body', 'recommending_text',)
    template_name = 'review/review_update.html'


class ReviewDeleteView(LoginRequiredMixin, CustomUserPassTestMixin, ReviewSidebarMixin, generic.DeleteView):
    """
    レビューの削除view
    """
    model = Review
    template_name = 'review/review_delete.html'
    success_url = reverse_lazy('books:home')


class ReviewDetailGetView(ReviewSidebarMixin, generic.DetailView):
    """
    レビューの詳細ページへのリクエストメソッドがGETの時のview。
    この時にレビューへのコメントフォームを追加する。
    """
    model = Review
    template_name = 'review/review_detail.html'

    def get_context_data(self, **kwargs):
        """
        CommentFormを追加。
        リクエストメソッドがPOSTの時にこのフォームが使用される。
        """
        context = super().get_context_data(**kwargs)
        context['form']  = CommentForm()
        return context   


class ReviewDetailPostView(SingleObjectMixin, ReviewSidebarMixin, FormView):
    """
    レビューの詳細ページへのリクエストメソッドがPOSTの時のview
    """
    model = Review
    form_class = CommentForm
    template_name = 'review/review_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.review = self.object
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('review:detail', kwargs={'pk': self.object.pk})


class ReviewDetailView(LoginRequiredMixin, generic.View):
    """
    レビューの詳細ページへのview
    リクエストのメソッドがGetかPostに応じて異なるビューを呼び出す。
    Get -> ReviewDetailGetView
    Post - > ReviewDetailPostView
    """
    def get(self, request, *args, **kwargs):
        view = ReviewDetailGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewDetailPostView.as_view()
        return view(request, *args, **kwargs)


class LikeView(LoginRequiredMixin, AjaxPostRequiredMixin, generic.View):
    """
    レビューのLikeするときのview
    """
    def post(self, request, *args, **kwargs):
        review_id = request.POST.get('id')
        action = request.POST.get('action')
        review = get_object_or_404(Review, id=review_id)

        if action == 'like':
            Like.objects.create_like(user=self.request.user, review=review)
        else:
            Like.objects.filter(user=self.request.user, review=review).delete()
        return JsonResponse({'status': 'ok'})
