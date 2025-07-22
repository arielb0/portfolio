from django.urls import path
from .views import CreateSurvey, DetailSurvey, UpdateSurvey, DeleteSurvey, ListSurvey, SubmitSurvey
from .views import CreateQuestion, DetailQuestion, UpdateQuestion, DeleteQuestion, ListQuestion
from .views import CreateAnswer, DetailAnswer, UpdateAnswer, DeleteAnswer, ListAnswer
from .views import FaqView

app_name = 'feedback'

urlpatterns = [
    path('survey/create', CreateSurvey.as_view(), name = 'survey_create'),
    path('survey/<int:pk>/detail', DetailSurvey.as_view(), name = 'survey_detail'),
    path('survey/<int:pk>/update', UpdateSurvey.as_view(), name = 'survey_update'),
    path('survey/<int:pk>/delete', DeleteSurvey.as_view(), name = 'survey_delete'),
    path('', ListSurvey.as_view(), name = 'survey_list'),
    path('survey/<int:pk>/submit', SubmitSurvey.as_view(), name='survey_submit'),
    path('question/create', CreateQuestion.as_view(), name = 'question_create'),
    path('question/<int:pk>/detail', DetailQuestion.as_view(), name = 'question_detail'),
    path('question/<int:pk>/update', UpdateQuestion.as_view(), name = 'question_update'),
    path('question/<int:pk>/delete', DeleteQuestion.as_view(), name = 'question_delete'),
    path('question', ListQuestion.as_view(), name = 'question_list'),
    path('answer/create', CreateAnswer.as_view(), name = 'answer_create'),
    path('answer/<int:pk>/detail', DetailAnswer.as_view(), name = 'answer_detail'),
    path('answer/<int:pk>/update', UpdateAnswer.as_view(), name = 'answer_update'),
    path('answer/<int:pk>/delete', DeleteAnswer.as_view(), name = 'answer_delete'),
    path('answer', ListAnswer.as_view(), name = 'answer_list'),
    path('faq', FaqView.as_view(), name = 'faq')
]
