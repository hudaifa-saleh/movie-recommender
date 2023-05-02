import csv
import datetime
from pprint import pprint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from faker import Faker

User = get_user_model()


def get_recent_users(days_ago=7, ids_only=True):
    delta = datetime.timedelta(days=days_ago)
    time_delta = timezone.now() - delta
    qs = User.objects.filter(Q(date_joined__gte=time_delta) | Q(last_login__gte=time_delta))
    if ids_only:
        return qs.values_list("id", flat=True)
    return qs


def get_fake_profiles(count=10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        data = {"username": profile.get("username"), "email": profile.get("mail"), "is_active": True}
        if "name" in profile:
            fname, lname = profile.get("name").split(" ")[:2]
            data["first_name"] = fname
            data["last_name"] = lname
        user_data.append(data)
    return user_data
