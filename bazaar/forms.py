from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import Field, ModelForm
from django.forms.utils import ErrorList
from .models import Currency, Category, Ad, Report
from django.forms.widgets import TextInput, Textarea, NumberInput, Select, EmailInput, SelectMultiple, ClearableFileInput, HiddenInput

class CurrencyForm(ModelForm):
    
    class Meta:
        model = Currency
        fields = ['name', 'code']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'code': TextInput(attrs={'class': 'form-control'})
        }

class CategoryForm(ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        '''
            I overwrite this method to specify parent_category queryset
            to avoid circular dependency. When you updated a Category, 
            you can't select their parents.

            Returns
            -------
            None
        '''
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        if instance:
            ancestors_pk = []
            ancestors_pk.append(instance.pk)
            category = instance
            parent = instance.parent_category

            while parent:
                ancestors_pk.append(parent.pk)
                category = parent
                parent = category.parent_category
        
            self.fields['parent_category'].queryset = Category.objects.exclude(pk__in=ancestors_pk)
        

    class Meta:
        model = Category
        fields = ['name', 'picture', 'priority', 'parent_category']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'picture': ClearableFileInput(attrs={'class': 'form-control'}),
            'priority': NumberInput(attrs={'class': 'form-control'}),
            'parent_category': Select(attrs={'class': 'form-select'})
        }

class AdForm(ModelForm):

    class Meta:
        model = Ad
        fields = [
            'title', 'description', 'price', 'currency', 'address', 'name',
            'phone', 'mail', 'alternative_currencies', 'category', 
            'picture_0', 'picture_1', 'picture_2', 'picture_3', 
            'picture_4', 'picture_5', 'picture_6', 'picture_7', 
            'picture_8', 'picture_9'
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'currency': Select(attrs={'class': 'form-select'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'phone': NumberInput(attrs={'class': 'form-control'}),
            'mail': EmailInput(attrs={'class': 'form-control'}),
            'alternative_currencies': SelectMultiple(attrs={'class': 'form-select'}), # I think could be better use select box (CheckboxSelectMultiple).
            'category': Select(attrs={'class': 'form-select'}),
            'picture_0': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_1': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_2': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_3': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_4': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_5': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_6': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_7': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_8': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_9': ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ReportForm(ModelForm):
    
    class Meta:
        model = Report
        fields = ['reason', 'description', 'ad']
        widgets = {
            'reason': Select(attrs={'class': 'form-select'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'ad': HiddenInput()
        }


