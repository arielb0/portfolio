from django import forms
from django.forms import widgets

class MovieForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=32, required=True, label='', widget=widgets.TextInput({'class': 'form-control', 'placeholder': 'Search a movie by title'}))