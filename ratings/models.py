from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg

User = settings.AUTH_USER_MODEL


class RatingChoice(models.IntegerChoices):
    ONE = 1
    TOW = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class RatingQuerySet(models.QuerySet):
    def avg(self):
        return self.aaggregate(avg=Avg("value"))["average"]


class RatingManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return RatingQuerySet(self.model, using=self._db)

    def rating(self):
        return self.get_queryset().avg()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(blank=True, null=True, choices=RatingChoice.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RatingManager()  # Rating.objects.rating()

    def __str__(self) -> str:
        return f"{self.user} | {self.value}"
