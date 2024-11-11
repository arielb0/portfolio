from django.urls import path, include
from .views import CreateReview, DetailReview, UpdateReview, DeleteReview, ListReview
from .views import Home
from .views import ReviewViewSet, AnswerViewSet, QuestionViewSet, DataViewSet
from rest_framework import routers

app_name = 'restaurant'

router = routers.DefaultRouter()
router.register(r'review', ReviewViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'data', DataViewSet)

urlpatterns = [
    path('', Home.as_view(), name='home'), # Keep this endpoint (static)
    path('review/create', CreateReview.as_view(), name='review_create'),
    path('review/<int:pk>', DetailReview.as_view(), name='review_detail'),
    path('review/<int:pk>/update', UpdateReview.as_view(), name='review_update'),
    path('review/<int:pk>/delete', DeleteReview.as_view(), name='review_delete'),
    path('review', ListReview.as_view(), name='review_list'),
    path('api/', include(router.urls)) # Keep this endpoint (dinamic)
]
