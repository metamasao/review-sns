from pyexpat import model
from django.views import generic
from django.shortcuts import get_object_or_404

from .models import Book, Category
from .forms import BookForm


class BookListHomeView(generic.ListView):
    model = Book
    template_name = 'books/home.html'
    context_object_name = 'books'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        category_pk = self.kwargs.get('pk')
        if category_pk:
            category = get_object_or_404(Category, id=category_pk)
            queryset = queryset.filter(category=category)
        return queryset


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category
        same_category_books = Book.objects.filter(category=category).exclude(id=self.object.id)
        context['same_category_books'] = same_category_books[:5]
        return context
        
class BookCreateView(generic.CreateView):
    form_class = BookForm
    template_name = 'books/book_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_books = Book.objects.all().order_by('-created')[:3]
        context['recent_books'] = recent_books
        return context
