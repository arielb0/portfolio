from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from .models import Review, Answer, Question, Data
from .forms import ReviewForm
from django.urls import reverse_lazy
from .serializers import ReviewSerializer, AnswerSerializer, QuestionSerializer, DataSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from string import Template

# Create your views here.

class CreateReview(CreateView):
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('restaurant:home')

class DetailReview(DetailView):
    model = Review

class UpdateReview(UpdateView):
    model = Review
    form_class = Review
    success_url = reverse_lazy('restaurant:home')

class DeleteReview(DeleteView):
    model = Review
    success_url = reverse_lazy('restaurant:home')

class ListReview(ListView):
    model = Review

class Home(TemplateView):
    template_name = 'restaurant/home.html'

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.all()
        if reviews.count() != 0:
            context['customer_satisfaction'] = round(reviews.filter(sentiment=1).count() * 5 / reviews.count(), 0)
        else:
            context['customer_satisfaction'] = 0
        context['review_form'] = ReviewForm
        context['reviews'] = reviews
        return context
    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
# Protect this view using authentication
class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def chat(self, request, pk = None):
        
        try:
            answer = Answer.objects.get(pk=pk)
        except:
            raise NotFound(detail='No Answer matches the given query')
        
        template = Template(answer.body)
        identifiers = template.get_identifiers()
        mapping = {}

        for identifier in identifiers:
            try:
                mapping[identifier] = Data.objects.get(key = identifier).value
            except:
                mapping[identifier] = 'identifier_not_found'

        answer.body = template.substitute(mapping)

        return Response(AnswerSerializer(answer).data)

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class DataViewSet(ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer