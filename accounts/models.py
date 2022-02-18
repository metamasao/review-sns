from django.contrib.auth.models import AbstractUser
from django.db import models

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
        return 'accounts:detail'    


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
