from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import MovieForm
from .helpers import MovieRecommenderEngine

recommender_engine = MovieRecommenderEngine()

# Create your views here.

class SearchFormView(FormView):
    template_name = 'movie/search.html'
    form_class = MovieForm


class SearchResultView(FormView):
    template_name = 'movie/search_result.html'
    form_class = MovieForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if 'title' in self.request.GET.keys():
            context['movies'] = recommender_engine.search_movie(self.request.GET['title'], 10)

        return context
    
        # I need to use a library to integrate Django and Pandas (django_pandas)
        

class MovieDetailView(TemplateView):
    template_name = 'movie/detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # You need to retrieve from dataset a movie, using a unique identifier
        # (tconst)
        # Then you need to search similar movies and put on view context.
        
        context = super().get_context_data(**kwargs)       
        movie = recommender_engine.get_movie(kwargs['id'])
        movie_recommendations = recommender_engine.get_recommendations(movie, 10)
        context['movie'] = movie.iloc[0].to_dict()
        context['recommendations'] = movie_recommendations
        
        return context
