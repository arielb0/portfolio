from django.forms import Form, ModelForm, CharField, IntegerField, DateField, ModelChoiceField, ModelMultipleChoiceField
from .models import Currency, Category, Ad, Report, Profile, Review
from django.forms.widgets import TextInput, Textarea, NumberInput, Select, SelectMultiple, ClearableFileInput, HiddenInput
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _

class CurrencyForm(ModelForm):
    
    class Meta:
        model = Currency
        fields = ['name', 'code']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'code': TextInput(attrs={'class': 'form-control'})
        }

class CategoryForm(ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        '''
            I overwrite this method to specify parent_category queryset
            to avoid circular dependency. When you update a Category model, 
            exlude himself and their childrens from parent_category field.
        '''

        def get_subcategories(category: Category) -> list[int]:
            '''
                Given a category model, return all subcategories id related to them.               

                Parameters
                ----------
                category: Category 
                    The category that you need to get all subcategories.

                Returns:
                --------
                list[int]
                    A list of primary keys of all subcategories, related to input category.
            '''

            subcategories = category.subcategories.all()
            
            categories_pk = [category.pk]

            for subcategory in subcategories:
                categories_pk.append(subcategory.pk)
                if len(subcategory.subcategories.all()) != 0:
                    categories_pk.append(get_subcategories(subcategory))
            
            return categories_pk
            
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        if instance:
            self.fields['parent_category'].queryset = Category.objects.exclude(pk__in=get_subcategories(instance))

    class Meta:
        model = Category
        fields = ['name', 'description', 'picture', 'priority', 'parent_category']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs = {'class': 'form-control'}),
            'picture': ClearableFileInput(attrs={'class': 'form-control'}),
            'priority': NumberInput(attrs={'class': 'form-control'}),
            'parent_category': Select(attrs={'class': 'form-select'})
        }

class AdForm(ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        '''
            I modify this constructor to return only the leaf categories
            (Categories that does not have children and does not have priority)
        '''

        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.filter(subcategories = None)

    class Meta:
        model = Ad
        fields = [
            'title', 'description', 'price', 'currency', 
            'alternative_currencies', 'category', 
            'picture_0', 'picture_1', 'picture_2', 'picture_3', 
            'picture_4', 'picture_5', 'picture_6', 'picture_7', 
            'picture_8', 'picture_9'
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'currency': Select(attrs={'class': 'form-select'}),
            'alternative_currencies': SelectMultiple(attrs={'class': 'form-select'}),
            'category': Select(attrs={'class': 'form-select'}),
            'picture_0': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_1': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_2': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_3': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_4': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_5': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_6': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_7': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_8': ClearableFileInput(attrs={'class': 'form-control'}),
            'picture_9': ClearableFileInput(attrs={'class': 'form-control'}),
        }

class AdStatusForm(ModelForm):

    class Meta:
        model = Ad
        fields = ['status']
        widgets = {
            'status': HiddenInput(),
        }

class ReportForm(ModelForm):
    
    class Meta:
        model = Report
        fields = ['reason', 'description', 'ad']
        widgets = {
            'reason': Select(attrs={'class': 'form-select'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'ad': HiddenInput()
        }

class SimpleSearchForm(Form):
    query = CharField(label = _('Query'), required = False, widget = TextInput(attrs={'class': 'form-control me-2'}))

class AdvancedSearchForm(SimpleSearchForm):
    price_start = IntegerField(label = _('Price start'), required = False, widget = NumberInput(attrs={'class': 'form-control'}))
    price_end = IntegerField(label = _('Price end'), required = False, widget = NumberInput(attrs={'class': 'form-control'}))
    currencies = ModelMultipleChoiceField(label = _('Currencies'), required = False, queryset=Currency.objects.all(), widget = SelectMultiple(attrs={'class': 'form-select'}), to_field_name = 'slug')
    address = CharField(label = _('Address'), required = False, widget = TextInput(attrs={'class': 'form-control'}))
    date_start = DateField(label = _('Date start'), required = False, widget = DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_end = DateField(label = _('Date end'), required = False, widget = DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    category = ModelChoiceField(label = _('Category'), required = False, queryset = Category.objects.filter(subcategories = None), widget = Select(attrs={'class': 'form-select'}), to_field_name = 'slug')

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['address', 'phone']
        widgets = {
            'address': TextInput(attrs = {'class': 'form-control'}),
            'phone': TextInput(attrs = {'class': 'form-control'})
        }

class ReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'comment', 'reviewed']
        widgets = {
            'rating': Select(attrs={'class': 'form-control'}),
            'comment': Textarea(attrs={'class': 'form-control'}),
            'reviewed': HiddenInput(),
        }    