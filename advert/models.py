from django.db import models
from common.models import TimestampedModel


class Category(TimestampedModel):
    name = models.CharField()


class City(TimestampedModel):
    name = models.CharField()


class Advert(TimestampedModel):
    title = models.CharField()
    description = models.TextField()
    city = models.ForeignKey(
        City, blank=True, null=True,
        on_delete=models.SET_NULL, related_name="talk_price_data"
    )
    category = models.ForeignKey(
        Category, blank=True, null=True,
        on_delete=models.SET_NULL, related_name="talk_price_data"
    )
    views = models.PositiveBigIntegerField(default=0)

