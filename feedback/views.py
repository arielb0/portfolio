from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, FormView, TemplateView
from .forms import SurveyForm, QuestionForm, AnswerForm
from .models import Survey, Question, Answer, Data
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from .helpers import create_form, get_stats, get_charts
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class CreateSurvey(LoginRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    success_url = reverse_lazy('feedback:survey_list')

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

class DetailSurvey(UserPassesTestMixin, DetailView):
    model = Survey

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = get_stats(self.get_object())
        context['charts'] = get_charts(self.get_object())
        
        return context
    
    def test_func(self):
        # A user can see survey statistics if is the survey owner or survey is open
        survey = self.get_object()
        return self.request.user.pk == survey.user.pk or survey.open

class UpdateSurvey(UserPassesTestMixin, UpdateView):
    model = Survey
    form_class = SurveyForm
    success_url = reverse_lazy('feedback:survey_list')

    def test_func(self):
        return self.request.user == self.get_object().user

class DeleteSurvey(UserPassesTestMixin, DeleteView):
    model = Survey
    success_url = reverse_lazy('feedback:survey_list')

    def test_func(self):
        return self.request.user == self.get_object().user

class ListSurvey(ListView):
    model = Survey

class SubmitSurvey(FormView):
    template_name = 'feedback/survey_submit.html'
    success_url = reverse_lazy('feedback:survey_list')

    def get_form_class(self):
        return create_form(Survey.objects.get(pk=self.kwargs['pk']))
    
    def form_valid(self, form):

        for key, value in form.cleaned_data.items():
            if key != 'captcha':
                if type(value) == list:
                    for single_value in value: # Useful for fields that allow several values (Checkbox)
                        data = Data.objects.create(question= Question.objects.get(slug=key), answer=single_value)
                        data.save()
                else:
                    data = Data.objects.create(question= Question.objects.get(slug=key), answer=value)
                    data.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Survey.objects.get(pk=self.kwargs['pk']).title
        return context

class CreateQuestion(UserPassesTestMixin, CreateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('feedback:question_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['survey'].queryset = Survey.objects.filter(user=self.request.user)
        return form

    def test_func(self):        
        if 'data' in self.get_form_kwargs().keys():
            survey_pk = self.get_form_kwargs()['data']['survey']            
            
            try:
                survey = Survey.objects.get(pk=survey_pk)
                return survey.user == self.request.user
            except:
                return False
        
        return True
            
class DetailQuestion(DetailView): # TODO: This view has no purpose.
    model = Question

class UpdateQuestion(UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('feedback:question_list')

    def test_func(self):
        return self.request.user == self.get_object().survey.user

class DeleteQuestion(UserPassesTestMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('feedback:question_list')

    def test_func(self):
        return self.request.user == self.get_object().survey.user

class ListQuestion(LoginRequiredMixin, ListView):
    model = Question

    def get_queryset(self):
        return Question.objects.filter(survey__user=self.request.user)

class CreateAnswer(UserPassesTestMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    success_url = reverse_lazy('feedback:answer_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['question'].queryset = Question.objects.filter(survey__user=self.request.user)
        return form
    
    def test_func(self):
                
        if 'data' in self.get_form_kwargs().keys():
            question_pk = self.get_form_kwargs()['data']['question']
            
            try:
                question = Question.objects.get(pk=question_pk)
                return question.survey.user == self.request.user
            except:
                return False
        
        return True

class DetailAnswer(DetailView): # TODO: This view does not have purpose. Delete it
    model = Answer

class UpdateAnswer(UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    success_url = reverse_lazy('feedback:answer_list')

    def test_func(self):
        return self.request.user == self.get_object().question.survey.user

class DeleteAnswer(UserPassesTestMixin, DeleteView):
    model = Answer
    success_url = reverse_lazy('feedback:answer_list')

    def test_func(self):
        return self.request.user == self.get_object().question.survey.user

class ListAnswer(LoginRequiredMixin, ListView):
    model = Answer
    success_url = reverse_lazy('feedback:answer_list')

    def get_queryset(self):
        return Answer.objects.filter(question__survey__user=self.request.user)
    
class FaqView(TemplateView):
    template_name = 'feedback/faq.html'