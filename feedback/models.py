from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify

class Survey(models.Model):
    title = models.CharField(verbose_name = _('Title'), max_length = 128)
    description = models.TextField(verbose_name = _('Description'), max_length= 255)
    open = models.BooleanField(verbose_name = _('Open'))
    user = models.ForeignKey(verbose_name = _('User'), to = User, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.title}'

class Question(models.Model):
    survey = models.ForeignKey(verbose_name = _('Survey'), to = Survey, on_delete = models.CASCADE)
    text = models.CharField(verbose_name = _('Text'), max_length = 128)
    slug = models.SlugField()
    index = models.IntegerField(verbose_name= _('Index'), default=0)
    class FieldTypeChoices(models.TextChoices):
        SELECT = 'SL', _('Select')
        RADIO_SELECT = 'RS', _('Radio Select')
        CHECK_BOX = 'CB', _('Check Box')
        NUMBER_INPUT = 'NI', _('Number Input')
    field_type = models.CharField(verbose_name = _('Type'), max_length = 2, choices = FieldTypeChoices)
    min_value = models.IntegerField(verbose_name = _('Min value'), default=0)
    max_value = models.IntegerField(verbose_name = _('Max value'), default=255)

    def __str__(self):
        return f'{self.survey.title} - {self.text}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        return super().save(*args, **kwargs)

class Answer(models.Model):
    question = models.ForeignKey(verbose_name = _('Question'), to = Question, on_delete = models.CASCADE)
    text = models.TextField(verbose_name = _('Text'))

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.question}: {self.text}'

class Data(models.Model):
    question = models.ForeignKey(verbose_name = _('Question'), to = Question, on_delete = models.CASCADE)
    answer = models.IntegerField(verbose_name = _('Answer'))

    def __str__(self):
        return f'{self.question.survey}, {self.question}, {self.answer}'