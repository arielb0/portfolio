from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    title = models.CharField("Title", max_length=50)
    body = models.TextField("Body")
    tags = models.CharField("Tags", max_length=50)
    date = models.DateField("Date", auto_now=False, auto_now_add=False)
    time = models.TimeField("Time", auto_now=False, auto_now_add=False)
    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.CASCADE)

    def __str__(self):
        return self.title[0:9]