from django.urls import path
from .views import CreateReview, DetailReview, UpdateReview, DeleteReview, ListReview
from .views import Home

app_name = 'restaurant'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('review/create', CreateReview.as_view(), name='review_create'),
    path('review/<int:pk>', DetailReview.as_view(), name='review_detail'),
    path('review/<int:pk>/update', UpdateReview.as_view(), name='review_update'),
    path('review/<int:pk>/delete', DeleteReview.as_view(), name='review_delete'),
    path('review', ListReview.as_view(), name='review_list'),
]
