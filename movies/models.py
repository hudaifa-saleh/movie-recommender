import datetime

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from ratings.models import Rating

RATING_CALC_TIME_IN_DAYS = 1


class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = GenericRelation(Rating)
    rating_last_updated = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    rating_avg = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    rating_count = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.title} | {self.id}"

    def rating_avg_display(self):
        now = timezone.now()
        if not self.rating_last_updated:
            return self.calculate_rating()
        if self.rating_last_updated > now - datetime.timedelta(days=RATING_CALC_TIME_IN_DAYS):
            return self.rating_avg
        return self.calculate_rating()

    def calculate_ratings_count(self):
        return self.ratings.all().count()

    def calculate_ratings_avg(self):
        return self.ratings.all().avg()

    def calculate_rating(self, save=True):
        rating_avg = self.calculate_ratings_avg()
        rating_count = self.calculate_ratings_count()
        self.rating_count = rating_count
        self.rating_avg = rating_avg
        self.rating_last_updated = timezone.now()
        if save:
            self.save()
        return self.rating_avg
