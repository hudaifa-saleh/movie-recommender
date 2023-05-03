from movies.models import Movie


def task_calculate_movie_ratings(all=False, count=None):
    qs = Movie.objects.all()
    if all:
        qs = Movie.objects.all()
    qs = qs.order_by("rating_last_updated")

    if isinstance(count, int):
        qs = qs[:count]

    for obj in qs:
        obj.calculate_ratings(save=True)
