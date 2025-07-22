from django.forms import ModelForm
from .models import Survey, Question, Answer
from django.forms.widgets import TextInput, Textarea, Select, CheckboxInput, NumberInput
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV3

class SurveyForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = Survey
        fields = ['title', 'description', 'open']
        widgets = {
            'title': TextInput(attrs = {'class': 'form-control'}),
            'description': Textarea(attrs = {'class': 'form-control'}),
            'open': CheckboxInput(attrs={'class': 'form-check-input'}),
            'captcha': TextInput()
        }

class QuestionForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    
    class Meta:
        model = Question
        fields = ['survey', 'text', 'index', 'field_type', 'min_value', 
                  'max_value']
        widgets = {
            'survey': Select(attrs = {'class': 'form-select'}),
            'text': TextInput(attrs = {'class': 'form-control'}),
            'index': NumberInput(attrs = {'class': 'form-control'}),
            'field_type': Select(attrs = {'class': 'form-control'}),
            'min_value': NumberInput(attrs = {'class': 'form-control'}),
            'max_value': NumberInput(attrs = {'class': 'form-control'}),
        }

class AnswerForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = Answer
        fields = ['question', 'text']
        widgets = {
            'question': Select(attrs = {'class': 'form-control'}),
            'text': TextInput(attrs = {'class': 'form-control'}),
        }