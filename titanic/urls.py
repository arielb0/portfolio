from django.urls import path
from titanic import views

app_name = 'titanic'

urlpatterns = [
    path('', views.UserForm.as_view(), name='form'),
    path('prediction', views.UserPrediction.as_view(), name='prediction')
]
