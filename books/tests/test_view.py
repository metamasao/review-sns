import logging
from unittest import mock
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from books.views import BookListHomeView
from books.models import Book, Category

fmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'
logging.basicConfig(level='DEBUG', format=fmt)
logger = logging.getLogger(__name__)

def create_category():
    for i in range(4):
        Category.objects.create(category=f'category {i}')
    return Category.objects.all()

@mock.patch.object(Book, 'get_book_info')
def create_books(get_book_info):
    category_queryset = Category.objects.all()
    k = 0
    for i in range(1,21):
        category = category_queryset[k]
        if i % 5 == 0:
            k += 1
        get_book_info.return_value = {
            'title': f'test title{i}',
            'cover': f'https://book.com/cover{i}'
        }
        book = Book(isbn=f'{1234567891123 + i}', category=category)
        book.save()
        logger.debug(f'title: {book.title} cover: {book.image_url} category: {book.category}')
    return Book.objects.all()


class BookViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.category_queryset = create_category()
        self.book_queryset = create_books()

    def test_book_list_home_view(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = BookListHomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data['books'], self.book_queryset[:10].order_by('-created'))
        self.assertEqual(response.context_data['nav_page'], 'home')