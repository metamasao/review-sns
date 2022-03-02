from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Category
from .forms import BookForm
from accounts.models import Action
from core.viewmixin import NavPageMixin, AuthorMixin
from review.models import Review


class BookListHomeView(NavPageMixin, generic.ListView):
    model = Book
    template_name = 'books/home.html'
    context_object_name = 'books'
    paginate_by = 10
    nav_page = 'home'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_pk = self.kwargs.get('pk')
        if category_pk:
            category = get_object_or_404(Category, id=category_pk)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_queryset = Category.objects.order_by_the_number_of_books()
        order_by_the_number_of_reviews = Book.objects.order_by_the_number_of_reviews()[:5]
        review_order_by_the_number_of_likes = Review.objects.order_by_the_number_of_likes()[:5]
        context['category_queryset'] = category_queryset
        context['order_by_the_number_of_reviews'] = order_by_the_number_of_reviews
        context['review_order_by_the_number_of_likes'] = review_order_by_the_number_of_likes
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        same_category_books = Book.objects.get_same_category_books(instance=self.object)
        context['same_category_books'] = same_category_books
        return context
        
class BookCreateView(LoginRequiredMixin, NavPageMixin, AuthorMixin, generic.CreateView):
    form_class = BookForm
    template_name = 'books/book_create.html'
    nav_page = 'create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_books = Book.objects.all()[:3]
        context['recent_books'] = recent_books
        return context

    def form_valid(self, form):
        valid = super().form_valid(form)
        Action.objects.create_action(self.request.user, self.object)
        return valid
