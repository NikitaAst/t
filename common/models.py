from django.db import models
from uuid import uuid4
from django.contrib.postgres.indexes import BrinIndex


class UUIDModel(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModel(UUIDModel):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        indexes = (
            BrinIndex(fields=['created_at']),
        )
        ordering = ['-created_at', '-updated_at']
