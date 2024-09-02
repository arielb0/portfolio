from django.db import models
from datetime import datetime
from .helpers import make_inference

# Create your models here.

class Review(models.Model):
    name = models.TextField(max_length=128)
    email = models.EmailField()
    body = models.TextField(max_length=255)
    prediction = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        return f'{self.body[0:16]}'
        
    def save(self):
        self.prediction = make_inference(self.body)
        if self.prediction == 0:
            print('The application will notify to restaurant owner..')
        return super().save()
