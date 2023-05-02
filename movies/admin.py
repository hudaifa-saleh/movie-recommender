from django.contrib import admin

from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id", "rating_avg", "rating_count"]
    readonly_fields = ["id", "rating_avg", "rating_count"]
    search_fields = ["id"]


admin.site.register(Movie, MovieAdmin)
