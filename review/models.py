from django.db import models
from django.conf import settings

from accounts.models import Action
from books.models import Book
from core.behaviors import (
    UUIDURLModel,
    AuthorModel,
    ActiveModel,
    TimeStampModel,
    PublishModel,
    PublishManager
)


class LikeManager(models.Manager):

    def create_like(self, user, review):
        like = self.model(
            user=user,
            review=review
        )
        like.save()
        Action.objects.create_action(user, review)
        return like


class Review(
    UUIDURLModel,
    AuthorModel,
    ActiveModel,
    TimeStampModel,
    PublishModel
):
    related_book = models.ForeignKey(
        Book,
        related_name='review_reviews',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    next_book = models.ForeignKey(
        Book,
        related_name='review_next_book',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=127)
    body = models.TextField()
    recommending_text = models.CharField(max_length=255)
    review_likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Like',
        related_name='user_likes',
        symmetrical=False,
    )
    
    objects = PublishManager()

    @property
    def url_name(self):
        return 'review:detail'


class Like(TimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )

    objects = LikeManager()

    def __str__(self):
        return f'{self.user.username} liked {self.review.title}'


