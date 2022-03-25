from django.contrib.auth.models import AbstractUser
from django.db import models

from books.models import Book
from core.behaviors import UUIDURLModel, TimeStampModel, AuthorModel


class CustomUser(AbstractUser, UUIDURLModel):    
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

    def create_follow(self, user_from, user_to):
        following = self.model(
            user_from=user_from,
            user_to=user_to
        )
        following.save()
        Action.objects.create_action(user_from, user_to)
        return following


class Follow(TimeStampModel):

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

    def get_following_actions(self, request_user):
        user_following = request_user.following.all()
        return self.filter(author__in=user_following)

    def get_action_content(self, user, instance):
        content = None
        if isinstance(instance, CustomUser):
            name = instance.username
            content = f'{user.username}さんが{name}さんをフォローしました。'
            return content
        name = instance.title
        content = f'{user.username}さんが{name}をいいねしました。'
        return content

    def create_action(self, user, instance):
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
    action_content = models.CharField(max_length=512)
    action_url = models.URLField()

    objects = ActionManager()

    def __str__(self):
        return self.action_content
