from django.shortcuts import render
from django.views import generic

from movies.models import Movie


class MovieListView(generic.ListView):
    template_name = "movies/movie_list.html"
    paginate_by = 50
    # context = {}
    queryset = Movie.objects.all().order_by("-rating_avg")


movie_list_view = MovieListView.as_view()


class MovieDetailView(generic.DetailView):
    template_name = "movies/movie_detail.html"
    # context = {}
    queryset = Movie.objects.all()


movie_detail_view = MovieDetailView.as_view()
