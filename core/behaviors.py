import datetime
import uuid
from django.db import models
from django.db.models import Count
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
    

class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class UUIDURLModel(UUIDModel):

    class Meta:
        abstract = True

    @property
    def url_name(self):
        raise NotImplementedError('オーバーライドしてください')

    def get_url_kwargs(self, **kwargs):
        kwargs.update(getattr(self, 'url_kwargs', {}))
        return kwargs

    def get_absolute_url(self):
        url_kwargs = self.get_url_kwargs(pk=self.id) 
        return reverse(self.url_name, kwargs=url_kwargs)


class AuthorModel(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)ss',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created',)


class PublishModel(models.Model):

    STATUS = (
        ('draft', 'draft'),
        ('public', 'public'),
    )

    status = models.CharField(max_length=6, choices=STATUS, default='draft')
    published = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.status=='public' and not self.published:
            self.published = timezone.now()
        super().save(*args, **kwargs)

    @property
    def published_recently(self):
        return (self.published > timezone.now() - datetime.timedelta(days=3)) if self.published is not None else None


class PublishManager(models.Manager):

    def public(self):
        return self.filter(status='public')
        
    def draft(self):
        return self.filter(status='draft')


        
