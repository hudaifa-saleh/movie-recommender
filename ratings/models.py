from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.utils import timezone

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
    active_update_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = RatingManager()  # Rating.objects.rating()

    def __str__(self) -> str:
        return f"{self.user} | {self.value}"

    class Meta:
        ordering = ["-timestamp"]


def rating_post_save(sender, instance, created, *args, **kwargs):
    if created:
        _id = instance.id
        if instance.active:
            qs = Rating.objects.filter(
                content_type=instance.content_type,
                object_id=instance.object_id,
                user=instance.user,
            ).exclude(id=_id, active=True)
            if qs.exists():
                qs = qs.exclude(active_update_timestamp__isnull=False)
                qs.update(active=False, active_update_timestamp=timezone.now())


post_save.connect(rating_post_save, sender=Rating)
