from typing import Any, List

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic

from movies.models import Movie

SORTING_CHOICES = {
    "popular": "popular",
    "unpopular": "unpopular",
    "top rated": "-rating_avg",
    "low rated": "rating_avg",
    "recent": "-release_date",
    "old": "release_date",
}


class MovieListView(generic.ListView):
    # template_name = "movies/list-view.html"
    paginate_by = 50
    # context = {}

    def get_queryset(self):
        request = self.request
        default_sort = request.session.get("movie_sort_order") or "-rating_avg"
        qs = Movie.objects.all().order_by(default_sort)
        sort = request.GET.get("sort")
        if sort is not None:
            request.session["movie_sort_order"] = sort
            qs = qs.order_by(sort)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        context["sorting_choices"] = SORTING_CHOICES
        if user.is_authenticated:
            object_list = context["object_list"]
            object_ids = [x.id for x in object_list]
            my_ratings = user.rating_set.movies().as_object_dict(object_ids=object_ids)
            context["my_ratings"] = my_ratings
        return context

    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ["movies/snippet/list.html"]
        return ["movies/list-view.html"]


movie_list_view = MovieListView.as_view()


class MovieDetailView(generic.DetailView):
    template_name = "movies/movie_detail.html"
    # context = {}
    queryset = Movie.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            object = context["object"]
            object_ids = [object.id]
            my_ratings = user.rating_set.movies().as_object_dict(object_ids=object_ids)
            context["my_ratings"] = my_ratings
        return context


movie_detail_view = MovieDetailView.as_view()


class MovieInfininteRatingView(MovieDetailView):
    def get_object(self):
        user = self.request.user
        exclude_ids = []
        if user.is_authenticated:
            exclude_ids = [x.object_id for x in user.rating_set.filter(active=True)]
        return Movie.objects.all().exclude(id__in=exclude_ids).order_by("?").first()

    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ["movies/snippet/infinte.html"]
        return ["movies/infinte-view.html"]


movie_infinte_view = MovieInfininteRatingView.as_view()
