from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea, EmailInput
from .models import Review

class ReviewForm(ModelForm):
    
    class Meta:
        model = Review
        fields = ['name', 'email', 'body']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'body': Textarea(attrs={'class': 'form-control'}),
        }
        