import logging
from unittest import mock
from django.test import TestCase
from django.db.models import Count

from books.models import Book, Category

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

def create_category():
    for i in range(2):
        Category.objects.create(category=f'category {i}')
    return Category.objects.all()

@mock.patch.object(Book, 'get_book_info')
def create_book(get_book_info):
    category = Category.objects.all()
    for i in range(10):
        get_book_info.return_value = {
            'title': f'title {i}',
            'cover': f'https://api.coverexample.com/cover{i}',
            'author': f'author {i}'
        }
        book = Book(
            isbn=f'{1234567891123 + i}',
            category=category[0] if i < 6 else category[1]
        )
        book.save()
        logger.info(f'title: {book.title} category: {book.category.category} cover: {book.image_url} isbn: {book.isbn}')
    return Book.objects.all()

class BookModelTest(TestCase):

    def setUp(self):
        self.category_queryset = create_category()
        self.book_queryset = create_book()
        self.category = self.category_queryset[0]
        self.book = self.book_queryset[0]

    def test_category_manager_method(self):
        category_queryset = Category.objects.annotate(related_books_counts=Count('books_books')).order_by('-related_books_counts')
        self.assertQuerysetEqual(
            Category.objects.order_by_the_number_of_books(), 
            category_queryset,
            transform=lambda x: x)
    
    def test_book_manager_method(self):
        same_category_books = Book.objects.filter(category=self.book.category).exclude(id=self.book.id).order_by('-created')[:5]
        self.assertQuerysetEqual(
            same_category_books, 
            Book.objects.get_same_category_books(instance=self.book),
            transform=lambda x: x)

    def test_category_model(self):
        for i, category in enumerate(self.category_queryset):
            self.assertEqual(category.category, f'category {i}')

    def test_book_model(self):
        for i, book in enumerate(self.book_queryset):
            self.assertEqual(book.title, f'title {9-i}')
            self.assertEqual(book.image_url, f'https://api.coverexample.com/cover{9-i}')
            self.assertEqual(book.isbn, f'{1234567891123 + (9-i)}')
            self.assertEqual(
                book.category.category,
                'category 1' if i < 4 else 'category 0'
            )
            self.assertEqual(book.__str__(), book.title)
            self.assertEqual(book.url_name, 'review:book-detail')