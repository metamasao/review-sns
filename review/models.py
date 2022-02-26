from django.db import models

from books.models import Book
from core.behaviors import (
    UUIDModel,
    AuthorModel,
    ActiveModel,
    TimeStampModel,
    PublishModel,
    PublishManager
)


class Review(
    UUIDModel,
    AuthorModel,
    ActiveModel,
    TimeStampModel,
    PublishModel
):
    related_book = models.ForeignKey(
        Book,
        related_name='reviews_reviews',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    next_book = models.ForeignKey(
        Book,
        related_name='reviews_next_book',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=127)
    body = models.TextField()
    recomending_text = models.CharField(max_length=255)
    
    objects = PublishManager()