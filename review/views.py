from django.urls import reverse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from books.models import Book
from core.viewmixin import AuthorMixin
from .models import Review
from .forms import ReviewModelForm, CommentForm


class ReviewCreateView(AuthorMixin, generic.CreateView):
    form_class = ReviewModelForm
    template_name = 'review/review_create.html'

    def form_valid(self, form):
        next_book = Book.objects.get(isbn=form.cleaned_data['isbn'])
        related_book = Book.objects.get(pk=self.kwargs.get('pk'))
        form.instance.related_book = related_book
        form.instance.next_book = next_book
        return super().form_valid(form)


class ReviewDetailGetView(generic.DetailView):
    model = Review
    template_name = 'review/review_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']  = CommentForm
        return context   


class ReviewDetailPostView(SingleObjectMixin, FormView):
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
        return reverse('review:detail', kwargs={'pk': self.object.pk})


class ReviewDetailView(generic.View):

    def get(self, request, *args, **kwargs):
        view = ReviewDetailGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewDetailPostView.as_view()
        return view(request, *args, **kwargs)