from django.db import models

from core.behaviors import (
    UUIDModel,
    AuthorModel,
    ActiveModel,
    TimeStampModel,
    PublishModel,
)


class Review(
    UUIDModel,
    AuthorModel,
    ActiveModel,
    TimeStampModel,
    PublishModel
):
    title = models.CharField(max_length=127)