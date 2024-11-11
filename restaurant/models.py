from django.db import models
from datetime import datetime
from .helpers import make_inference, MLClassifier
from random import choice

# Create your models here.

class Base(models.Model):
    body = models.TextField(max_length=255)
    prediction = models.IntegerField(null=True, editable = False)
    datetime = models.DateTimeField(default=datetime.now, null=True, editable = False)

    class Meta:
        abstract = True

class Review(Base):
    name = models.TextField(max_length=128)
    email = models.EmailField()
    prediction = None
    sentiment = models.BooleanField()

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        return f'{self.body[0:16]}'
    
class Answer(Base):
    prediction = None
    datetime = None
    topic_choices =  {
        0: 'unknown',
        1: 'user_satisfaction',
        2: 'opening_hours',
        3: 'address',
        4: 'contact',
        5: 'menu',
        6: 'reservation',
        7: 'home_delivery',
        8: 'services',
        9: 'thanks_answer',
        10: 'positive_review',
        11: 'negative_review',
        12: 'alergens',
        13: 'pets',
        14: 'dressing',
        15: 'children',
        16: 'smoking',
        17: 'parking',
        18: 'disability'
    }
    topic = models.IntegerField(choices = topic_choices)

    def __str__(self):
        return f'{self.topic}: {self.body[:16]}'
    
class Question(Base):
    user = models.TextField(max_length = 255, null = True, editable = False)
    answer = models.ForeignKey(to = Answer, blank = True, null = True, on_delete = models.CASCADE)

    class Meta:
        ordering = ['-datetime']

    def save(self, *args, **kwargs):
        
        classifation_result = MLClassifier.classify_text(self.body)
        highest_probability = MLClassifier.get_highest_prob(classifation_result[1][0])
        answers = Answer.objects.filter(topic = classifation_result[0])

        if highest_probability > 0.6:
            self.prediction = classifation_result[0]
        else:           
            self.prediction = 0

        self.answer = choice(answers)

        return super().save()

class Data(models.Model):
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
