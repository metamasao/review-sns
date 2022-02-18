from django.db import models

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
    title = models.CharField(max_length=127)