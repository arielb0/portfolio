from typing import Any
from django.forms import ModelForm, TextInput, Textarea
from note.models import Note

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body', 'tags']
        widgets = {            
            'title': TextInput(attrs={'class': 'form-control'}),
            'tags': TextInput(attrs={'class': 'form-control'}),
            'body': Textarea(attrs={'class': 'form-control'}),
        }
