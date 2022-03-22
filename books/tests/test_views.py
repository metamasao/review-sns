import logging
from unittest import mock
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from books.views import BookListHomeView, BookCreateView
from books.models import Book, Category

fmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'
logging.basicConfig(level='DEBUG', format=fmt)
logger = logging.getLogger(__name__)

def create_category():
    for i in range(2):
        Category.objects.create(category=f'category {i}')
    return Category.objects.all()

@mock.patch.object(Book, 'get_book_info')
def create_books(get_book_info):
    category= Category.objects.all()
    for i in range(20):
        get_book_info.return_value = {
            'title': f'test title{i}',
            'cover': f'https://book.com/cover{i}',
            'author': f'test author{i}'
        }
        book = Book(
            isbn=f'{1234567891123 + i}', 
            category=category[0] if i < 12 else category[1]
        )
        book.save()
        logger.debug(f'title: {book.title} cover: {book.image_url} category: {book.category}')
    return Book.objects.all().order_by('-created',)


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
        self.book = self.book_queryset[0]
        self.category = self.category_queryset[0]

    def test_book_list_home_view(self):
        request = self.factory.get('/')
        response = BookListHomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['nav_page'], 'home')
        self.assertIn('category_queryset', response.context_data)
        with self.assertTemplateUsed('books/home.html'):
            response.render()
        with self.assertTemplateNotUsed('books/book_home.html'):
            response.render()
        for book in self.book_queryset[:10]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, 'Wrong title')
    
    def test_book_list_home_search_result_based_on_the_title(self):
        request = self.factory.get(f'/?query={self.book.title}')
        response = BookListHomeView.as_view()(request)
        search_result_book = response.context_data['books'][0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(search_result_book.title, self.book.title)
        self.assertEqual(search_result_book.author, self.book.author)
        self.assertNotEqual(search_result_book.title, self.book_queryset[1].title)
        self.assertNotEqual(search_result_book.author, self.book_queryset[1].author)

    def test_book_list_home_search_result_based_on_the_author(self):
        request = self.factory.get(f'/query={self.book.author}')
        response = BookListHomeView.as_view()(request)
        search_result_book = response.context_data['books'][0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(search_result_book.title, self.book.title)
        self.assertEqual(search_result_book.author, self.book.author)
        self.assertNotEqual(search_result_book.title, self.book_queryset[1].title)
        self.assertNotEqual(search_result_book.author, self.book_queryset[1].author)
        
    def test_book_list_home_view_given_page(self):
        request = self.factory.get('/?page=2')
        response = BookListHomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        for book in self.book_queryset[10:]:
            self.assertContains(response, book.title)

    def test_book_list_home_view_given_category(self):
        request = self.factory.get('/')
        category = self.category
        response = BookListHomeView.as_view()(request, pk=category.pk)
        self.assertEqual(response.status_code, 200)
        for book in response.context_data['books']:
            self.assertEqual(book.category.category, category.category)
    
    def test_book_create_view_get(self):
        request = self.factory.get('/create/')
        request.user = self.user
        response = BookCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('recent_books', response.context_data)
        with self.assertTemplateUsed('books/book_create.html'):
            response.render()

    def test_book_create_view_post_invalid_data(self):
        client = Client()
        client.login(username='testuser', password='testpass123')
        response = client.post(
            '/create/',
            data={
                'title': 'Test book name',
                'isbn': '12345678d1123'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'isbn', '13桁の数字のみを入力してください。')