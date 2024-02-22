from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.SearchFormView.as_view(), name='search_form'),
    path('search_result/', views.SearchResultView.as_view(), name='search_result'),
    path('<id>/', views.MovieDetailView.as_view(), name='detail')
]
