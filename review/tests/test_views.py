import logging
from unittest import mock
from django.test import RequestFactory, TestCase, Client
from django.contrib.auth import get_user_model

from books.models import Book, Category
from review.views import (
    ReviewCreateView,
    ReviewDeleteView,
    ReviewDetailView,
    ReviewListView, 
    ReviewAuthorDetailView, 
    ReviewBookDetailView,
    ReviewUpdateView
)
from review.models import Review

fmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'
logging.basicConfig(level='DEBUG', format=fmt)
logger = logging.getLogger(__name__)

@mock.patch.object(Book, 'get_book_info')
def create_books(get_book_info):
    for i in range(2):    
        category = Category.objects.create(category=f'category {i}')
        get_book_info.return_value = {
            'title': f'title {i}',
            'cover': f'https://api.example.com/cover{i}',
            'author': f'author {i}'
        }
        book = Book(
            isbn=f'{1234567891123 + i}',
            category=category
        )
        book.save()
        logger.debug(f'title: {book.title} cover: {book.image_url} author: {book.author}')
    return Book.objects.all()

def create_reviews(author, book_set):
    related_book = book_set[0]
    next_book = book_set[1]
    for i in range(20):
        Review.objects.create(
            author=author,
            related_book=related_book,
            next_book=next_book,
            title=f'review title {i}',
            body= f'review body {i}' if i < 15 else f'review body draft {i}',
            recommending_text=f'A next book is {next_book.title}',
            status='public' if i < 15 else 'draft'
        )
    return Review.objects.all()
        

class ReviewViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.review_author = get_user_model().objects.create_user(
            username='review_author',
            email='review_author@email.com',
            password='testpass123'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.book_set = create_books()
        self.related_book = self.book_set[0]
        self.next_book = self.book_set[1]
        self.review_set = create_reviews(author=self.review_author, book_set=self.book_set)
        self.draft_review_set = Review.objects.draft()
        self.public_review_set = Review.objects.public()
        self.review = self.public_review_set[0]

    def test_review_list_view(self):
        request = self.factory.get('/review/')
        request.user = self.user
        response = ReviewListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('following_actions', response.context_data)
        self.assertIn('popular_reviews', response.context_data)
        self.assertIn('nav_page', response.context_data)
        with self.assertTemplateUsed('review/review_list.html'):
            response.render()
        with self.assertTemplateNotUsed('review/wrong.html'):
            response.render()
        for public_review in self.public_review_set[:10]:
            self.assertContains(response, public_review.title)
            self.assertContains(response, public_review.body)
        for draft_review in self.draft_review_set:
            self.assertNotContains(response, draft_review.title)
            self.assertNotContains(response, draft_review.body)

    def test_review_list_view_page2(self):
        request = self.factory.get('/review/?page=2')
        request.user = self.user
        response = ReviewListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        for review in self.public_review_set[11:]:
            self.assertContains(response, review.title)
            self.assertContains(response, review.body)
        
    def test_review_author_detail_view_requested_by_author(self):
        request = self.factory.get(f'/review/{self.review_author.pk}/author-detail/')
        request.user = self.review_author
        response = ReviewAuthorDetailView.as_view()(request, pk=self.review_author.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('author', response.context_data)
        self.assertIn('author_popular_reviews', response.context_data)
        with self.assertTemplateUsed('review/review_author_detail.html'):
            response.render()
        with self.assertTemplateNotUsed('review/wrong.html'):
            response.render()
        for draft_review in self.draft_review_set:
            self.assertContains(response, draft_review.body)
        for review in self.review_set[:10]:
            self.assertContains(response, review.body)

    def test_review_author_detail_view_requested_by_user(self):
        request = self.factory.get(f'/review/{self.review_author.pk}/author-detail/')
        request.user = self.user
        response = ReviewAuthorDetailView.as_view()(request, pk=self.review_author.pk)
        self.assertEqual(response.status_code, 200)
        for draft_review in self.draft_review_set:
            self.assertNotContains(response, draft_review.body)
        for review in self.public_review_set[:10]:
            self.assertContains(response, review.title)
            self.assertContains(response, review.body)

    def test_review_book_detail_view(self):
        request = self.factory.get(f'/review/{self.related_book.pk}/book-detail/')
        request.user = self.user
        response = ReviewBookDetailView.as_view()(request, pk=self.related_book.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('book', response.context_data)
        with self.assertTemplateUsed('review/review_book_detail.html'):
            response.render()
        for review in self.public_review_set[:10]:
            self.assertContains(response, review.title)
            self.assertContains(response, review.body)
        
    def test_review_create_view_get(self):
        request = self.factory.post(f'/review/{self.related_book.pk}/create/')
        request.user = self.user
        response = ReviewCreateView.as_view()(request, pk=self.related_book.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['form'].__class__.__name__, 'ReviewModelForm')
        with self.assertTemplateUsed('review/review_create.html'):
            response.render()
        with self.assertTemplateNotUsed('review/wrong.html'):
            response.render()

    def test_review_create_view_post_valid_data(self):
        request = self.factory.post(
            f'/review/{self.related_book.pk}/create/',
            data={
                'title': 'test review title',
                'body': 'test review body',
                'status': 'public',
                'isbn': f'{self.next_book.isbn}',
                'recommending_text': 'You should read this book!'
            }
        )
        request.user = self.review_author
        response = ReviewCreateView.as_view()(request, pk=self.related_book.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.public_review_set[0].title, 'test review title')

    def test_review_create_view_post_invalid_data_object_does_not_exist(self):
        client = Client()
        client.login(username='review_author', password='testpass123')
        response = client.post(
            f'/review/{self.related_book.pk}/create/',
            data={
                'title': 'test review title',
                'body': 'test review body',
                'status': 'public',
                'isbn': '9999999999999',
                'recommending_text': 'You can not find this next_book'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form', 
            'isbn', 
            '該当する本が当サイトに登録されていません。ページ上部のナビゲーションバーから本を登録してください。'
        )

    def test_review_create_view_post_invalid_data_not_only_figures(self):
        client = Client()
        client.login(username='review_author', password='testpass123')
        response = client.post(
            f'/review/{self.related_book.pk}/create/',
            data={
                'title': 'test review title',
                'body': 'test review body',
                'status': 'public',
                'isbn': '12345678911d3',
                'recommending_test': 'invalid',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'isbn', '13桁の数字のみを入力してください。')

    def test_review_update_view(self):
        request = self.factory.get(f'/review/{self.review.pk}/update/')
        request.user = self.review_author
        response = ReviewUpdateView.as_view()(request, pk=self.review.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', response.context_data['form'].fields)
        self.assertIn('body', response.context_data['form'].fields)
        self.assertIn('recommending_text', response.context_data['form'].fields)
        with self.assertTemplateUsed('review/review_update.html'):
            response.render()
        with self.assertTemplateNotUsed('review/wrong.html'):
            response.render()

    def test_review_delete_view(self):
        request = self.factory.get(f'/review/{self.review.pk}/delete/')
        request.user = self.review_author
        response = ReviewDeleteView.as_view()(request, pk=self.review.pk)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('review/review_delete.html'):
            response.render()
        with self.assertTemplateNotUsed('review/wrong.html'):
            response.render()

    def test_review_detali_view_get(self):
        request = self.factory.get(f'/review/{self.review.pk}/detail/')
        request.user = self.user
        response = ReviewDetailView.as_view()(request, pk=self.review.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['form'].__class__.__name__, 'CommentForm')
        with self.assertTemplateUsed('review/review_detail.html'):
            response.render()
        with self.assertTemplateNotUsed('review/wrong.html'):
            response.render()