from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse

from core.behaviors import UUIDModel, TimeStampModel


class CustomUser(AbstractUser, UUIDModel):
    
    following = models.ManyToManyField(
        'self',
        through='Follow',
        related_name='followers',
        symmetrical=False
    )

    def get_absolute_url(self):
        return reverse("detail", kwargs={
            'pk': self.pk,
            'username': self.username
        })
    


class FollowManager(models.Manager):

    def create_follow(self, user_from, user_to):
        following = self.model(
            user_from=user_from,
            user_to=user_to
        )
        following.save()
        Event.objects.create_event(user_from, user_to)
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

class EventManager(models.Manager):

    def get_event_content(self, user, instance):
        content = None
        if isinstance(instance, CustomUser):
            name = instance.username
            content = f'{user.username}さんが{name}さんをフォローしました。'
            return content        
        name = instance.title
        content = f'{user.username}さんが{name}をいいねしました。'
        return content

    def create_event(self, user, instance):
        content = self.get_event_content(user, instance)
        instance_url = instance.get_absolute_url()
        
        event = self.model(
            creator=user,
            event=content,
            event_url=instance_url
        )
        event.save()
        return event


class Event(TimeStampModel):
    
    creator = models.ForeignKey(
        CustomUser,
        related_name='events',
        on_delete=models.CASCADE
    )
    event = models.CharField(max_length=512)
    event_url = models.URLField()

    objects = EventManager()

    def __str__(self):
        return self.event[:50]
