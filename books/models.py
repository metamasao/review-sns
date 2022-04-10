import requests
import logging
from django.db import models
from django.db.models import Count

from core.behaviors import UUIDModel, UUIDURLModel, TimeStampModel

logger = logging.getLogger(__name__)


class CategoryManager(models.Manager):
    """
    カテゴリーマネージャー
    """
    def order_by_the_number_of_books(self):
        """
        各カテゴリーに登録された本の総数を返す。
        """
        queryset = self.annotate(related_books_counts=Count('books_books'))
        return queryset.order_by('-related_books_counts')


class BookManager(models.Manager):
    """
    ブックマネージャー
    """
    def get_same_category_books(self, instance, index=5):
        """
        各本のカテゴリーと同じカテゴリーの本を返す。ただし、instanceは除く。
        """
        return self.filter(category=instance.category).exclude(id=instance.id)[:index]

    def order_by_the_number_of_reviews(self):
        """
        各本の公開レビューの総数から降順に本のクエリセットを返す。
        """
        queryset = self.filter(
            review_reviews__status='public'
            ).annotate(related_reviews_counts=Count('review_reviews'))
        return queryset.order_by('-related_reviews_counts')


class Category(UUIDModel):
    """
    カテゴリーモデル。

    主な属性の説明
    ----------
    books_books: Bookモデルとの一対多関係
    マネージャーはCategoryManagerを使用
    """
    category = models.CharField(max_length=31, unique=True)

    objects = CategoryManager()

    def __str__(self):
        return self.category


class Book(TimeStampModel, UUIDURLModel):
    """
    Bookモデル
    本の情報の取得に外部APIのOpenBDを使用しています。
    """
    author = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, unique=True)
    image_url = models.URLField(blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(
        Category,
        related_name='%(app_label)s_%(class)ss',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    objects = BookManager()

    @property
    def url_name(self):
        return 'review:book-detail'

    def __str__(self):
        return self.title

    def get_book_info(self):
        """
        formで入力された一意のisbnをもとにOpenBDからデータを取得する。
        レスポンスが200台以外のエラーであれば、Sentryがログを取得しメールにて通知する。
        """
        api_url = f'https://api.openbd.jp/v1/get?isbn={self.isbn}'
        try:
            logger.info('Attempting to connect to openbd.')
            response = requests.get(api_url)
            response.raise_for_status()
            response_data = response.json()[0]
            return response_data.get('summary') if response_data is not None else None
        except requests.exceptions.HTTPError as e:
            logger.exception(e)
            logger.error('Connecting to openbd fails.')
            return None

    def save(self, *args, **kwargs):
        book_info = self.get_book_info()
        if book_info:
            self.title = book_info.get('title')[:256]
            self.image_url = book_info.get('cover')
            self.author = book_info.get('author', '著者不明')
        super().save(*args, **kwargs)
    
