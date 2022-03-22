import logging
import datetime
import time
from unicodedata import category
from unittest import mock
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from books.models import Book, Category
from review.models import Review, Comment, Like

def create_category():
    category = Category.objects.create(category='test category')
    return category

@mock.patch.object(Book, 'get_book_info')
def create_books(get_book_info):
    category = create_category()
    for i in range(2):
        get_book_info.return_value = {
            'title': f'test book title{i}',
            'cover': f'https://api.bookcover.jp/testcover{i}',
            'author': f'test book author{i}',
        }
        book = Book(isbn=f'{1234567891123 + i}', category=category)
        book.save()
    return Book.objects.all()


class ReviewModelTest(TestCase):

    def setUp(self):
        self.book_queryset = create_books()
        self.related_book = self.book_queryset[0]
        self.next_book = self.book_queryset[1]
        self.author = get_user_model().objects.create_user(
            username='test author',
            email='testauthor@email.com',
            password='testpass123'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.review_liked = Review.objects.create(
            related_book=self.related_book,
            next_book=self.next_book,
            author=self.author,
            body='test body liked',
            recommending_text='test recommending text liked',
            status='public',
        )
        self.review = Review.objects.create(
            related_book=self.related_book,
            next_book=self.next_book,
            author=self.author,
            body='test body',
            recommending_text='test recommending text',
            status='draft'
        )
        self.comment = Comment.objects.create(
            author=self.user,
            review=self.review_liked,
            comment='A nice review'
        )
        self.like = Like.objects.create_like(
            user=self.user,
            review=self.review_liked
        )

    def test_review_model_manager_test(self):
        queryset_order_by_the_number_of_likes = Review.objects.filter(
            status='public'
        ).annotate(likes_counts=Count('review_likes')).order_by('-likes_counts')

        self.assertQuerysetEqual(
            Review.objects.order_by_the_number_of_likes(),
            queryset_order_by_the_number_of_likes,
            transform=lambda x: x
        )

    def test_like_model_manager(self):
        self.assertEqual(Like.objects.all().count(), 1)
        self.assertEqual(
            self.user.accounts_actions.all()[0].action_content,
            f'{self.user.username}さんが{self.review_liked.title}をいいねしました。'
        )

    def test_review_model_review_liked_and_public(self):
        review_liked = self.review_liked
        self.assertEqual(review_liked.status, 'public')
        self.assertEqual(review_liked.related_book, self.related_book)
        self.assertEqual(review_liked.next_book, self.next_book)
        self.assertEqual(review_liked.author, self.author)
        self.assertEqual(review_liked.body, 'test body liked')
        self.assertEqual(review_liked.recommending_text, 'test recommending text liked')
        self.assertEqual(review_liked.review_likes.all().count(), 1)
        self.assertEqual(review_liked.get_absolute_url(), f'/review/{review_liked.pk}/detail/')
        self.assertEqual(review_liked.modified_after_published, False)
        self.assertEqual(review_liked.__str__(), f'{review_liked.title} on {review_liked.related_book.title}')
        self.assertEqual(review_liked.review_comments.all().count(), 1)
        self.assertEqual(review_liked.published_recently, True)

    def test_review_model_modified(self):
        time.sleep(60)
        self.review_liked.save()
        self.assertEqual(self.review_liked.modified_after_published, True)

    def test_review_model_review_draft(self):
        review = self.review
        self.assertEqual(review.status, 'draft')
        self.assertEqual(review.published_recently, None)
        self.assertEqual(review.modified_after_published, None)
        self.assertEqual(review.review_likes.all().count(), 0)
        self.assertEqual(review.review_comments.all().count(), 0)

    def test_comment_model(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.review, self.review_liked)
        self.assertEqual(self.comment.comment, 'A nice review')
        self.assertEqual(self.comment.__str__(), f'comment on {self.review_liked.title}')

    def test_like_model(self):
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.review, self.review_liked)
        self.assertEqual(self.like.__str__(), f'{self.user.username} liked {self.review_liked.title}')