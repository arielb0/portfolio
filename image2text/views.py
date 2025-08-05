from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .forms import UploadImageForm
from django.urls import reverse_lazy
from .helpers import get_text_from_image
from django.forms import Form

# Create your views here.

class CreateRecognition(FormView):
    template_name = 'image2text/recognition_form.html'
    form_class = UploadImageForm
    success_url = reverse_lazy('image2text:text_detail')

    def form_valid(self, form: Form):
        image = form.cleaned_data['image']
        language = form.cleaned_data['language']
        self.request.session['recognition_result'] = get_text_from_image(image, language)
        return super().form_valid(form)
    

class TextDetail(TemplateView):
    template_name = 'image2text/text_detail.html'

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["recognition_result"] = self.request.session.pop('recognition_result', '')
        return context
    

class FaqView(TemplateView):
    template_name = 'image2text/faq.html'