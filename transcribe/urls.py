from django.urls import path
from .views import CreateTranscription, DetailTranscription, FaqView

app_name = 'transcribe'

urlpatterns = [
    path('', CreateTranscription.as_view(), name = 'transcription_create'),
    path('transcription/detail', DetailTranscription.as_view(), name = 'transcription_detail'),
    path('faq', FaqView.as_view(), name = 'faq')
]