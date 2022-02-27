from django.views import generic

from books.models import Book
from core.viewmixin import AuthorMixin
from .models import Review
from .forms import ReviewModelForm


class ReviewCreateView(AuthorMixin, generic.CreateView):
    form_class = ReviewModelForm
    template_name = 'review/review_create.html'

    def form_valid(self, form):
        next_book = Book.objects.get(isbn=form.cleaned_data['isbn'])
        related_book = Book.objects.get(pk=self.kwargs.get('pk'))
        form.instance.related_book = related_book
        form.instance.next_book = next_book
        return super().form_valid(form)


class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'review/review_detail.html'