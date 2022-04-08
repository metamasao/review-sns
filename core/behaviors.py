"""
DRYとFat Modelの設計思想に基づきこのモジュールを作りました。
また伝統的なFat Modelにおいても繰り返しを避けるために、Mix-inクラスを使っています。
ここで定義されたクラスを各アプリで継承しモデルを構築することで、シンプルで見やすく、
繰り返しを避けたアプリケーションを作ることができます。
"""


import datetime
import uuid
from django.db import models
from django.db.models import Count
from django.conf import settings
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
    

class UUIDModel(models.Model):
    """
    セキュリティ上の観点から単調増加キーではなくUUIDを主キーとする抽象モデル。
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class UUIDURLModel(UUIDModel):
    """
    UUIDモデルをベースとしget_absolute_urlメソッドを定義した抽象モデル。
    """
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
        return reverse_lazy(self.url_name, kwargs=url_kwargs)


class AuthorModel(models.Model):
    """
    CustomUserに紐づけられた著者抽象モデル。
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)ss',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    """
    必要に応じて悪質なコメントやアカウントなど利用を制限する抽象モデル。
    """
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class TimeStampModel(models.Model):
    """
    インスタンスの作成日時や更新日時を必要とするモデルに対する抽象モデル。
    複数の抽象クラスを継承する場合は、まず初めにこのクラスを継承する、
    もしくはMetaクラスで明示的に定義してください。
    参照: https://docs.djangoproject.com/en/4.0/topics/db/models/#model-inheritance-1
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # 降順
        ordering = ('-created',)


class PublishModel(models.Model):
    """
    記事などの公開・非公開を定め、初めて公開した場合にはその日時を保存する抽象モデル。
    """
    STATUS = (
        ('draft', 'draft'),
        ('public', 'public'),
    )

    status = models.CharField(max_length=6, choices=STATUS, default='draft')
    published = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # 初めて公開を選択した場合に、その日時を保存する。
        if self.status=='public' and not self.published:
            self.published = timezone.now()
        super().save(*args, **kwargs)

    @property
    def published_recently(self):
        """
        公開された日時が保存されており、その日時が3日以内であれば、Trueを返す。
        下書きを選択し、公開日時が保存されいないとき、Noneを返す。
        """
        return (self.published > timezone.now() - datetime.timedelta(days=3)) if self.published is not None else None


class PublishManager(models.Manager):
    """
    レビューや記事などのモデルでのマネージャーモデル。
    """
    def public(self):
        return self.filter(status='public')
        
    def draft(self):
        return self.filter(status='draft')


        
