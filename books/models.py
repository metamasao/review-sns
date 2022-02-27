import requests
import logging
from django.db import models
from django.db.models import Count

from core.behaviors import UUIDModel, UUIDURLModel, TimeStampModel

logger = logging.getLogger(__name__)


class CategoryManager(models.Manager):

    def order_by_the_number_of_books(self):
        queryset = self.annotate(related_books_counts=Count('books_books'))
        return queryset.order_by('-related_books_counts')


class BookManager(models.Manager):

    def get_same_category_books(self, instance, index=5):
        return self.filter(category=instance.category).exclude(id=instance.id)[:index]


class Category(UUIDModel):
    category = models.CharField(max_length=31, unique=True)

    objects = CategoryManager()

    def __str__(self):
        return self.category


class Book(UUIDURLModel, TimeStampModel):
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

    class Meta:
        ordering = ('-created',)

    @property
    def url_name(self):
        return 'books:detail'

    def __str__(self):
        return self.title

    def get_book_info(self):
        api_url = f'https://api.openbd.jp/v1/get?isbn={self.isbn}'
        response = requests.get(api_url)
        if response.status_code != 200:
            logger.warning('Something seems to be wrong with openbd.')
            return None
        
        response_data = response.json()[0]
        if response_data is None:
            return None
        return response_data.get('summary')

    def save(self, *args, **kwargs):
        book_info = self.get_book_info()
        if book_info:
            self.title = book_info.get('title')[:256]
            self.image_url = book_info.get('cover')
            self.author = book_info.get('author', '著者不明')
        super().save(*args, **kwargs)
        

