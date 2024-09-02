from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from .models import Review
from .forms import ReviewForm
from django.urls import reverse_lazy

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
        context['customer_satisfaction'] = round(Review.objects.filter(prediction=1).count() * 5 / reviews.count(), 0)
        context['review_form'] = ReviewForm
        context['reviews'] = reviews
        return context
