from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import UserForm
from .helpers import TitanicSurvivorModel

titanic_survivor = TitanicSurvivorModel()

# Create your views here.

class UserForm(FormView):
    template_name = 'titanic/user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('titanic:prediction')

    def form_valid(self, form: UserForm):

        # Retrieve form data.
        form_data = form.cleaned_data
        # Check if user will survive or not.
        prediction = titanic_survivor.predict(form_data)
        # Put the result on the user session.
        self.request.session['survived'] = prediction
        
        return super().form_valid(form)
    
        

class UserPrediction(TemplateView):
    template_name = 'titanic/user_prediction.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if 'survived' in self.request.session.keys():
            context['survived'] = self.request.session['survived']
            del self.request.session['survived']
        
        return context

