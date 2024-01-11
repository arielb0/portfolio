from typing import Any
from django.forms import ModelForm, TextInput, HiddenInput
from note.models import Note

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body', 'tags', 'date', 'time', 'owner']
        widgets = {
            'date': TextInput(attrs={'type': 'date'}),
            'time': TextInput(attrs={'type': 'time'}),
            'owner': HiddenInput()
        }
