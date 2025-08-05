from django.views.generic import TemplateView, FormView
from .forms import TranscribeForm
from django.urls.base import reverse_lazy
from .helpers import get_transcription

class CreateTranscription(FormView):
    form_class = TranscribeForm
    template_name = 'transcribe/transcription_form.html'
    success_url = reverse_lazy('transcribe:transcription_detail')

    def form_valid(self, form):
        transcription = get_transcription(form.cleaned_data['audio_file'])
        text_list = [sentence['text'] for sentence in transcription]
        self.request.session['transcription'] = '\n'.join(text_list)
        return super().form_valid(form)
    

class DetailTranscription(TemplateView):
    template_name = 'transcribe/transcription_detail.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["transcription"] = self.request.session.pop('transcription', "")
        return context
    
class FaqView(TemplateView):
    template_name = 'transcribe/faq.html'
    