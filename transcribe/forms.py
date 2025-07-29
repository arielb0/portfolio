from django.forms import Form
from django.forms.fields import FileField
from django.forms.widgets import FileInput
from django.core.validators import FileExtensionValidator

def validate_audio_file(value):
    print(type(value))

class TranscribeForm(Form):
    audio_file = FileField(widget=FileInput(attrs={'class': 'form-control', 'accept': 'audio/mpeg,audio/wav,audio/opus,audio/mp4,audio/aac,audio/flac,audio/3gpp,audio/amr'})
                           , validators=[FileExtensionValidator(['mp3', 'wav', 'opus', 'm4a', 'aac', 'flac', '3gp', 'amr'])])

    
    