from .models import Survey, Question, Answer, Data
from django.forms import Form, Field, CharField, ChoiceField, DecimalField, MultipleChoiceField
from django.forms.widgets import Select, RadioSelect, CheckboxSelectMultiple, NumberInput, Textarea, TextInput
from django.utils.text import slugify
from django.db.models import Avg, Count, Max, Min, StdDev, Sum, Variance, Q
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV3
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.utils.translation import gettext as _

def create_form(survey: Survey) -> Form:
    '''
        Creates a Django Form class based on Survey object.
    '''

    class DynamicForm(Form):
        pass

    DynamicForm.base_fields = {slugify(question.text): create_field(question) for question in Question.objects.filter(survey = survey).order_by('index')}
    DynamicForm.base_fields.update({'captcha': ReCaptchaField(widget=ReCaptchaV3)})

    return DynamicForm

def create_field(question: Question) -> Field:
    '''
        Creates a Django Form Field based on Question object.
    '''
        
    field = Field()
    field_type = question.field_type
    choices = [create_choice(answer) for answer in Answer.objects.filter(question = question).order_by('pk')]
    
    if field_type == 'SL':
        field = ChoiceField(choices=choices, widget=Select(attrs={'class': 'form-select'}))
    
    if field_type == 'RS':
        field = ChoiceField(choices=choices, widget=RadioSelect(attrs={'class': ''}, choices=choices))

    if field_type == 'CB':
        field = MultipleChoiceField(choices=choices)
        field.widget = CheckboxSelectMultiple(attrs={'class': ''}, choices=choices)

    if field_type == 'NI':
        field = DecimalField(min_value = question.min_value, max_value = question.max_value)
        field.widget = NumberInput(attrs={'class': 'form-control', 'min': question.min_value , 'max': question.max_value})        

    field.label = question.text
    field.required = True

    return field

def create_choice(answer: Answer) -> tuple:
    '''
        Create a tuple (key, value) based on Answer object.
    '''

    return (answer.pk, answer.text)

def get_stats(survey: Survey) -> dict:
    '''
        Given a survey, return statistics about collected data
    '''
    stats = dict()
    data = Data.objects.filter(question__survey=survey)
    
    for question_pk in data.values_list('question', flat=True).distinct('question'):
        '''
            Aggregate or statistics:

            OK Count
            OK Avg
            OK Max
            OK Min
            OK Sum
        '''
        question = Question.objects.get(pk=question_pk)

        if question.answer_set.count() > 0:
            '''
            Count table
            '''

            count = dict()
            for answer in Data.objects.filter(question=question_pk).values_list('answer', flat=True):
                
                try:
                    name = question.answer_set.get(pk=answer).text
                except:
                    name = answer

                answer_count = {name: Data.objects.filter(question=question_pk, answer=answer).count()}

                if question.text not in count.keys():
                    count[question.text] = answer_count
                else:
                    count[question.text].update(answer_count)
            
            
            if 'count' not in stats.keys():
                stats['count'] = count
            else:
                stats['count'].update(count)

        else:
            key_stats = {question.text: Data.objects.aggregate(min=Min('answer', filter=Q(question=question_pk)),
                                                 mean=Avg('answer', filter=Q(question=question_pk)),
                                                 max=Max('answer', filter=Q(question=question_pk)), 
                                                 count=Count('answer', filter=Q(question=question_pk)),
                                                 sum=Sum('answer', filter=Q(question=question_pk)),
                                                 std_dev=StdDev('answer', filter=Q(question=question_pk)),
                                                 variance=Variance('answer', filter=Q(question=question_pk)))}
            if 'key_stats' not in stats.keys():
                stats['key_stats'] = key_stats
            else:
                stats['key_stats'].update(key_stats)
            stats.update(key_stats)
        
    return stats

def get_charts(survey: Survey) -> dict:
    '''
        Given a survey return the charts (histogram for quantitative variable, bar chart for qualitative variable) about collected data.
    '''

    stats = dict()
    
    for question in Question.objects.filter(survey=survey):
        fig, ax = plt.subplots()

        if question.answer_set.count() > 0:
            # Qualitative variable (Bar chart)
            titles = [answer.text for answer in Answer.objects.filter(question=question)]
            count = [Data.objects.filter(question=question, answer=answer.pk).count() for answer in Answer.objects.filter(question=question)]
            ax.bar(titles, count, width=1)
        else:
            # Quantitative variable (Histogram)
            ax.hist(Data.objects.filter(question=question).values_list('answer', flat=True))

        ax.set_title(question.text)
        ax.set_xlabel(_('Value'))
        ax.set_ylabel(_('Count'))
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        base64_image = base64.b64encode(buffer.read()).decode('utf-8')

        stats.update({question.text: base64_image})
        plt.close(fig)

    return stats