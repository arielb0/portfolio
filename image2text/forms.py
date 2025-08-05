from django.forms import Form
from django.forms import FileField, ChoiceField
from django.forms.widgets import FileInput, Select
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

class UploadImageForm(Form):
    LANGUAGE_CHOICES = {
        'spa': _('Spanish'),
        'eng': _('English')
    }
    image = FileField(label=_('Image'), widget=FileInput(attrs={'class': 'form-control', 'accept': 'image/png,image/jpeg,image/tiff,image/gif,image/webp,image/bmp'})
                           , validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'tif', 'tiff', 'gif', 'webp', 'bmp'])])
    language = ChoiceField(label=_('Language'), widget=Select(attrs={'class': 'form-control'}), choices=LANGUAGE_CHOICES)