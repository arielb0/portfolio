from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea, EmailInput, RadioSelect
from .models import Review


class ReviewForm(ModelForm):
    
    class Meta:
        model = Review
        fields = ['name', 'email', 'sentiment', 'body']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'sentiment': RadioSelect(attrs={'class': 'form-check'}, choices = {1: 'True', 2: 'False'}),
            'body': Textarea(attrs={'class': 'form-control'}),
        }
        