"""
ThinViewにするためにできる限り必要なロジックをここに記述しています。
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from books.models import Book
from core.behaviors import UUIDURLModel, TimeStampModel, AuthorModel


class CustomUser(AbstractUser, UUIDURLModel):
    """
    DjangoのAbstractUser, coreパッケージの抽象モデルを継承しています。
    
    主な属性の説明
    --------
    following: 同一のモデルへの多対多関係
    user_likes: 「いいね」に関するレビューへの多対多関係
    review_reivews: 著者としてレビューへの一対多関係
    review_comments: コメントへの一対多関係

    """
    following = models.ManyToManyField(
        'self',
        through='Follow',
        related_name='followers',
        symmetrical=False
    )
    profile = models.CharField(blank=True, max_length=255)

    @property
    def url_name(self):
        return 'review:author-detail'

    @property
    def count_followings(self):
        return self.following.all().count()

    @property
    def count_followers(self):
        return self.followers.all().count()

    @property
    def count_reviews(self):
        review_set = self.review_reviews.all()
        return review_set.count()

    @property
    def count_review_likes(self):
        total_likes = 0
        review_set = self.review_reviews.all()
        
        for review in review_set:
            review_likes = review.review_likes.all()
            total_likes += review_likes.count()
        return total_likes


class FollowManager(models.Manager):
    """
    CustomUserモデルでのfollowingに対するマネージャーモデル。
    """
    def create_follow(self, user_from, user_to):
        """
        フォローする際に誰が誰をフォローしたのかをActionモデルに保存します。
        ※同じようなLikeモデルとLikeマネージャーモデルがあるので、
        これと併せてもう少し抽象化し、モデルを作成すべき
        """
        following = self.model(
            user_from=user_from,
            user_to=user_to
        )
        following.save()
        Action.objects.create_action(user_from, user_to)
        return following


class Follow(TimeStampModel):
    """
    CustomUserモデルのfollowingの中間モデル。この中間モデルを使うことで、
    詳細にモデルを定義できます。
    """
    user_from = models.ForeignKey(
        CustomUser,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        CustomUser,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )

    objects = FollowManager()

    def __str__(self):
        user_from_name = self.user_from.username
        user_to_name = self.user_to.username
        return f'{user_from_name} follows {user_to_name}'


class ActionManager(models.Manager):
    """
    Actionモデルのマネージャーモデル。ユーザーに応じたアクションを返すメソッド、
    具体的なアクションを記述するメソッドを定義しています。
    """
    def get_following_actions(self, request_user):
        """
        request_userがフォローしているひとのフォローやいいねといったアクションを返す。
        """
        user_following = request_user.following.all()
        return self.filter(author__in=user_following)

    def get_action_content(self, user, instance):
        """
        具体的なアクションの内容を条件に応して記述する。
        """
        content = None
        if isinstance(instance, CustomUser):
            name = instance.username
            content = f'{user.username}さんが{name}さんをフォローしました。'
            return content
        name = instance.title
        content = f'{user.username}さんが{name}をいいねしました。'
        return content

    def create_action(self, user, instance):
        """
        アクションの内容とその対象インスタンスのurlを取得しモデルとして保存する。
        """
        content = self.get_action_content(user, instance)
        instance_url = instance.get_absolute_url()
        
        action = self.model(
            author=user,
            action_content=content,
            action_url=instance_url
        )
        action.save()
        return action


class Action(TimeStampModel, AuthorModel):
    """
    CustomUserモデルのユーザーのAction(行動)を記録するモデル。
    DjangoのGenericForeginKeyを利用して簡明なモデルを作ることもできますが、
    ベストプラクティスに反するので、していません。
    参照: Daniel Roy GreenField, Audrey Roy Greenfield 
    'Two Scoops of Django 1.11' ch.6 4.6 'Try to Avoid Using Generic Relations'
    """
    action_content = models.CharField(max_length=512)
    action_url = models.URLField()

    objects = ActionManager()

    def __str__(self):
        return self.action_content
