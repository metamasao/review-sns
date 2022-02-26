from django.views import generic

from books.models import Book
from .forms import ReviewModelForm


class CreateReview(generic.CreateView):
    form_class = ReviewModelForm
    template_name = 'review/create_review.html'

    def form_valid(self, form):
        isbn = form.cleaned_data['isbn']
        book_pk = self.kwargs.get('pk')
        next_book = Book.objects.get(isbn=isbn)
        related_book = Book.objects.get(pk=book_pk)
        form.instance.related_book = related_book
        form.instance.next_book = next_book
        form.instance.author = self.request.user
        return super().form_valid(form)