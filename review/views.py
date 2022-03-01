from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from books.models import Book
from core.viewmixin import AuthorMixin, CustomUserPassTestMixin
from .models import Review
from .forms import ReviewModelForm, CommentForm


class ReviewCreateView(LoginRequiredMixin, AuthorMixin, generic.CreateView):
    form_class = ReviewModelForm
    template_name = 'review/review_create.html'

    def form_valid(self, form):
        next_book = get_object_or_404(
            Book,
            isbn=form.cleaned_data.get('isbn')
        )
        related_book = get_object_or_404(
            Book,
            pk=self.kwargs.get('pk')
        )
        form.instance.related_book = related_book
        form.instance.next_book = next_book
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, CustomUserPassTestMixin, generic.UpdateView):
    model = Review
    fields = ('title', 'body', 'recommending_text',)
    template_name = 'review/review_update.html'


class ReviewDeleteView(LoginRequiredMixin, CustomUserPassTestMixin, generic.DeleteView):
    model = Review
    template_name = 'review/review_delete.html'
    success_url = reverse_lazy('books:home')


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
        return reverse_lazy('review:detail', kwargs={'pk': self.object.pk})


class ReviewDetailView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        view = ReviewDetailGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewDetailPostView.as_view()
        return view(request, *args, **kwargs)


