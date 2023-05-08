import csv
import tempfile

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from django.db.models import F

from exports.models import Export
from ratings.models import Rating


def generate_rating_dataset(app_label="movies", model="movie"):
    ctype = ContentType.objects.get(app_label=app_label, model=model)
    qs = Rating.objects.filter(active=True, content_type=ctype)
    qs = qs.annotate(userId=F("user_id"), movieId=F("object_id"), rating=F("value"))
    return qs.values("userId", "movieId", "rating")


def export_dataset(dataset, fname="dataset.csv"):
    with tempfile.NamedTemporaryFile(mode="r+") as temp_f:
        try:
            keys = dataset[0].keys()
        except:
            return
        dict_writer = csv.DictWriter(temp_f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataset)
        temp_f.seek(0)  # go to the top of the file
        # write Export model
        obj = Export.objects.create(type=type)
        obj.file.save(fname, File(temp_f))
