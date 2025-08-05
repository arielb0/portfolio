from django.urls import path
from .views import CreateRecognition, TextDetail, FaqView

app_name = 'image2text'

urlpatterns = [
    path('', CreateRecognition.as_view(), name = 'recognition_create'),
    path('text/detail', TextDetail.as_view(), name = 'text_detail'),
    path('faq', FaqView.as_view(), name = 'faq')
]