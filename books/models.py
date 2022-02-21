from django.db import models
from django.db.models import Count

from core.behaviors import UUIDModel, UUIDURLModel, TimeStampModel
from .utils import get_book_info


class CategoryManager(models.Manager):

    def get_queryset_order_by_books(self):
        queryset = self.annotate(related_books_counts=Count('books_books'))
        return queryset.order_by('-related_books_counts')


class Category(UUIDModel):
    category = models.CharField(max_length=31, unique=True)

    objects = CategoryManager()

    def __str__(self):
        return self.category


class Book(UUIDURLModel, TimeStampModel):
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

    @property
    def url_name(self):
        return 'books:detail'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        response = get_book_info(isbn=self.isbn)
        if response is not None:
            book_summary = response.get('summary')
            self.title = book_summary.get('title')[:256]
            self.image_url = book_summary.get('cover')
        super().save(*args, **kwargs)
        

