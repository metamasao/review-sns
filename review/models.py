import datetime
from django.db import models
from django.db.models import Count
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


class ReviewManager(PublishManager):
    """
    Reviewモデルのマネージャー
    """
    def order_by_the_number_of_likes(self):
        """
        各レビューのLikeの総数に基づいて降順にクエリセットを返す。
        """
        queryset = self.filter(status='public').annotate(likes_counts=Count('review_likes'))
        return queryset.order_by('-likes_counts')


class LikeManager(models.Manager):
    """
    Likeモデルのマネージャー
    ユーザーのアクションも記録する。
    """
    def create_like(self, user, review):
        """
        Likeのインスタンスを生成し保存、ユーザーのアクション保存する。
        """
        like = self.model(user=user, review=review)
        like.save()
        Action.objects.create_action(user, review)
        return like


class Review(
    TimeStampModel,
    UUIDURLModel,
    AuthorModel,
    ActiveModel,
    PublishModel,
):
    """
    Reviewモデル
    Bookモデルについてのレビューを保存します。

    主な属性
    ----------
    author: レビューの著者、CustomUserモデルへの多対一関係
    related_book: レビューする本、Bookモデルへの多対一関係
    next_book: 次にお勧めする本、Bookモデルへへの多対一関係
    recommending_text: 次にお勧めする本への紹介文
    """
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
    
    objects = ReviewManager()

    def __str__(self):
        return f'{self.title} on {self.related_book.title}'

    @property
    def url_name(self):
        return 'review:detail'

    @property
    def modified_after_published(self):
        """
        公開後に記事内容を更新した場合にTrueを返す。
        """
        if self.published is None:
            return None
        return True if self.modified - self.published > datetime.timedelta(minutes=1) else False


class Like(TimeStampModel):
    """
    CustomUserモデルがReviewモデルをLikeするときの中間モデル。
    """
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


class Comment(TimeStampModel, AuthorModel, ActiveModel):
    """
    Reviewモデルに対するCommentモデル。

    主な属性
    ----------
    author: コメントの投稿者、CustomUserモデルへの多対一関係
    """
    review = models.ForeignKey(
        Review,
        related_name='review_comments',
        on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=255)

    def __str__(self):
        return f'comment on {self.review.title}'