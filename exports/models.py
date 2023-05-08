import pathlib
import uuid

from django.db import models
from django.utils import timezone


def export_file_handler(filename, instance, *args, **kwargs):
    today = timezone.now().strftime("%Y-%m-%d")
    fpath = pathlib.Path(filename)
    ext = fpath.suffix  # .csv
    dtype = instance.type
    if hasattr(instance, "id"):
        new_fname = f"{instance.id}{ext}"
    else:
        new_fname = f"{uuid.uuid4()}{ext}"
    return f"exports/{dtype}/{today}/{new_fname}"


class Export(models.Model):
    id = models.UUIDField(uuid.uuid4, editable=False, primary_key=True)
    file = models.FileField(upload_to=export_file_handler, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Export"
        verbose_name_plural = "Exports"

    def __str__(self):
        return self.id
