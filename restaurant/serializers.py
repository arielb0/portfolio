from .models import Review, Answer, Question, Data
from rest_framework import serializers

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'email', 'body', 'sentiment', 'datetime']

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'body', 'topic']

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answer = serializers.HyperlinkedRelatedField(view_name = 'restaurant:answer-detail'
                                                 , queryset = Answer.objects.all()
                                                 , allow_null = True)
    class Meta:
        model = Question
        fields = ['id', 'body', 'prediction', 'datetime', 'user', 'answer']

class DataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Data
        fields = ['id', 'key', 'value']
        