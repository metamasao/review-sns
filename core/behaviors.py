import datetime
import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


class ActiveManager(models.Manager):
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)
    

class UUIDModel(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class ActiveModel(models.Model):

    is_active = models.BooleanField(default=True)

    objects = ActiveManager()

    class Meta:
        abstract = True


class SlugModel(models.Model):

    slug = models.SlugField(
        max_length=127, 
        unique=True,
        blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug_source)
        super().save(*args, **kwargs)

    def get_url_kwargs(self, **kwargs):
        kwargs.update(getattr(self, 'url_kwargs', {}))
        return kwargs

    def get_absolute_url(self):
        url_kwargs = self.get_url_kwargs(slug=self.slug)
        return reverse(self.url_name, kwargs=url_kwargs)


class TimeStampModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishModel(models.Model):

    STATUS = (
        ('draft', 'draft'),
        ('public', 'public'),
    )

    status = models.CharField(max_length=6, choices=STATUS)
    published = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.published and self.status=='public':
            self.published = timezone.now()
        super().save(*args, **kwargs)

    @property
    def published_recently(self):
        return self.published > timezone.now() - datetime.timedelta(days=3)

"""
class Todo(
    ActiveModel,
    SlugModel,
    TimeStampModel,
    PublishModel,
    models.Model
):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='todos',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=127)
    body = models.TextField()
    user_liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked',
        blank=True
    )

    url_name = 'todo-post'

    @property
    def slug_source(self):
        return self.title

"""