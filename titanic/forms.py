from django import forms
from django.forms import widgets

class UserForm(forms.Form):
    
    passenger_class = forms.ChoiceField(
        required = True,
        choices = {'1': 'First', '2': 'Second', '3': 'Third'}, 
        label = 'Passenger class', 
        widget = forms.Select(attrs = {'class' : 'form-select'}))
    
    sex = forms.ChoiceField(
        required = True, 
        choices = {'0': 'Female', '1': 'Male'}, 
        label = 'Sex', 
        widget = forms.Select(attrs = {'class' : 'form-select'}))
    
    age = forms.IntegerField(
        required = True, 
        min_value = 1, 
        max_value = 120,
        widget = forms.NumberInput(attrs = {'class' : 'form-control'}))
    
    number_of_slibings_or_spouses = forms.IntegerField(
        required = True, 
        min_value = 0, 
        max_value = 20, 
        label = 'Number of slibings or spouses', 
        widget = forms.NumberInput(attrs = {'class': 'form-control'}))
    
    number_of_parents_or_children = forms.IntegerField(
        required = True, 
        min_value = 0, 
        max_value = 20, 
        label = 'Number of children or parents',
        widget = forms.NumberInput(attrs = {'class': 'form-control'}))
    
    fare = forms.IntegerField(
        required = True, 
        min_value = 0, 
        max_value = 500, 
        label = 'Fare',
        widget = forms.NumberInput(attrs = {'class': 'form-control'}))
    
    embarked = forms.ChoiceField(
        required = True, 
        choices = {'0': 'Cherbourg', '1': 'Queenstown', '2': 'Southampton'},
        label = 'Embarked',
        widget = forms.Select(attrs = {'class': 'form-select'}))
    