from django.test import TestCase
from ..forms import CurrencyForm, CategoryForm, AdForm, ReportForm, SimpleSearchForm, AdvancedSearchForm
from ..models import Currency, Category, Ad, Report
from django.forms import CharField, IntegerField, ModelChoiceField, DateField, ModelMultipleChoiceField
from django.forms.widgets import TextInput, Textarea, NumberInput, Select, EmailInput, SelectMultiple, ClearableFileInput, HiddenInput, DateInput

class CurrencyFormTestCase(TestCase):

    def test_currency_form_model(self):
        '''
            Test if CurrencyForm class use the correct model (Currency)
        '''

        self.assertEqual(CurrencyForm.Meta.model, Currency)

    def test_currency_form_fields(self):
        '''
            Test if CurrencyForm class use the correct fields (name, code)
        '''

        self.assertEqual(CurrencyForm.Meta.fields, ['name', 'code'])

    def test_currency_form_name_widget(self):
        '''
            Test if CurrencyForm class use the correct widget for name input (TextInput)
        '''

        self.assertEqual(CurrencyForm.Meta.widgets['name'].__class__, TextInput)

    def test_currency_form_code_widget(self):
        '''
            Test if CurrencyForm class use the correct widget for code input (TextInput)
        '''

        self.assertEqual(CurrencyForm.Meta.widgets['code'].__class__, TextInput)

class CategoryFormTestCase(TestCase):

    def test_init(self):
        '''
            Test if __init__ method implements the right logic
            (Given a Category model, exlude himself and their children from 
            parent_category field)
        '''

        groceries = Category(name = 'Groceries', priority = 1)
        groceries.save()
        drinks = Category(name = 'Drinks', parent_category = groceries)
        drinks.save()
        groceries_form = CategoryForm(instance=groceries)

        self.assertQuerySetEqual(groceries_form.fields['parent_category'].queryset, Category.objects.none())

    def test_category_form_model(self):
        '''
            Test if CategoryForm class use the correct model (Category)
        '''
        self.assertEqual(CategoryForm.Meta.model, Category)

    def test_category_form_fields(self):
        '''
            Test if CategoryForm class use the correct fields (name)
        '''

        self.assertEqual(CategoryForm.Meta.fields, ['name', 'picture', 'priority', 'parent_category'])

    def test_category_form_name_widget(self):
        '''
            Test if CategoryForm class use the correct widget for name input (TextInput)
        '''

        self.assertEqual(CategoryForm.Meta.widgets['name'].__class__, TextInput)

class AdFormTestCase(TestCase):

    def test_init(self):
        '''
            Test if __init__ method implements the right logic
            (Exclude from category selection, category models with childrens and priority)
        '''

        '''
            Pseudocode:

            Create parent category (Groceries).
            Save it.
            Create child category (drinks) and set groceries as parent category of drinks.
            Save it.
            Create a Ad "I sell ron" with category Drinks.
            Save it.
            Create a AdForm instantiating Ad.            
            Test if in AdForm appears Groceries (the rigth answer is no)
        '''

        groceries = Category(name = 'Groceries')

    
    def test_ad_form_model(self):
        '''
            Test if AdForm class use the correct model (Ad)
        '''

        self.assertEqual(AdForm.Meta.model, Ad)

    def test_ad_form_fields(self):
        '''
            Test if AdForm class use the correct form fields
            (title, description, price, currency, address, name,
            phone, mail, alternative_currencies, category, 
            picture_0, picture_1, picture_2, picture_3, 
            picture_4, picture_5, picture_6, picture_7, 
            picture_8, picture_9)
        '''

        form_fields = ['title', 'description', 'price', 'currency', 'address', 'name',
            'phone', 'mail', 'alternative_currencies', 'category', 
            'picture_0', 'picture_1', 'picture_2', 'picture_3',
            'picture_4', 'picture_5', 'picture_6', 'picture_7', 
            'picture_8', 'picture_9']
        
        self.assertEqual(AdForm.Meta.fields, form_fields)

    def test_ad_form_title_widget(self):
        '''
            Test if AdForm class use the correct widget for title field (TextInput)            
        '''

        self.assertEqual(AdForm.Meta.widgets['title'].__class__, TextInput)

    def test_ad_form_description_widget(self):
        '''
            Test if AdForm class use the correct widget for description field (TextArea)
        '''

        self.assertEqual(AdForm.Meta.widgets['description'].__class__, Textarea)

    def test_ad_form_price_widget(self):
        '''
            Test if AdForm class use the correct widget for price field (NumberInput)
        '''

        self.assertEqual(AdForm.Meta.widgets['price'].__class__, NumberInput)

    def test_ad_form_currency_widget(self):
        '''
            Test if AdForm class use the correct widget for currency field (Select)
        '''

        self.assertEqual(AdForm.Meta.widgets['currency'].__class__, Select)

    def test_ad_form_address_widget(self):
        '''
            Test if AdForm class use the correct widget for address field (TextInput)
        '''

        self.assertEqual(AdForm.Meta.widgets['address'].__class__, TextInput)

    def test_ad_form_name_widget(self):
        '''
            Test if AdForm class use the correct widget for name field (TextInput)
        '''

        self.assertEqual(AdForm.Meta.widgets['name'].__class__, TextInput)

    def test_ad_form_phone_widget(self):
        '''
            Test if AdForm class use the correct widget for phone field (NumberInput)
        '''

        self.assertEqual(AdForm.Meta.widgets['phone'].__class__, NumberInput)

    def test_ad_form_mail_widget(self):
        '''
            Test if AdForm class use the correct widget for mail field (EmailInput)
        '''

        self.assertEqual(AdForm.Meta.widgets['mail'].__class__, EmailInput)

    def test_ad_form_alternative_currencies_widget(self):
        '''
            Test if AdForm class use the correct widget for alternative_currencies field (SelectMultiple)
        '''

        self.assertEqual(AdForm.Meta.widgets['alternative_currencies'].__class__, SelectMultiple)

    def test_ad_form_category_widget(self):
        '''
            Test if AdForm class use the correct widget for category field (Select)
        '''

        self.assertEqual(AdForm.Meta.widgets['category'].__class__, Select)

    def test_ad_form_picture_n(self):
        '''
            Test if AdForm class use the correct widget for picture_n 
            (1 <= n < 11) (ClearableFileInput)
        '''

        for n in range(0, 10):
            self.assertEqual(AdForm.Meta.widgets[f'picture_{n}'].__class__, ClearableFileInput)

class ReportFormTestcase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_report_form_model(self):
        '''
            Test if ReportForm class use the correct model (Report)
        '''

        self.assertEqual(ReportForm.Meta.model, Report)

    def test_report_form_fields(self):
        '''
            Test if ReportForm class use the correct fields properties (reason, description, ad)
        '''

        self.assertEqual(ReportForm.Meta.fields, ['reason', 'description', 'ad'])

    def test_report_form_reason_widget(self):
        '''
            Test if ReportForm class use the correct widget for reason field (Select)
        '''

        self.assertEqual(ReportForm.Meta.widgets['reason'].__class__, Select)

    def test_report_form_description_widget(self):
        '''
            Test if ReportForm class use the correct widget for description field (Textarea)
        '''

        self.assertEqual(ReportForm.Meta.widgets['description'].__class__, Textarea)

    def test_report_form_ad_widget(self):
        '''
            Test if ReportForm class use the correct widget for ad field (HiddenInput).
        '''

        self.assertEqual(ReportForm.Meta.widgets['ad'].__class__, HiddenInput)

class SimpleSearchFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.simple_search_form = SimpleSearchForm()
        return super().setUpTestData()

    def test_simple_search_form_fields(self):
        '''
            Test if SimpleSearchForm form class has the correct fields
            (query)
        '''        

        self.assertIn('query', self.simple_search_form.fields.keys())

    def test_simple_search_form_query_field_class(self):
        '''
            Test if query form field use the correct class (CharField)
        '''

        self.assertIsInstance(self.simple_search_form.fields['query'], CharField)

    def test_simple_search_form_query_field_required(self):
        '''
            Test if query form field has required parameter set to false
        '''

        self.assertFalse(self.simple_search_form.fields['query'].required)

    def test_simple_search_form_query_field_widget(self):
        '''
            Test if query form field use the right widget (TextInput)
        '''

        self.assertIsInstance(self.simple_search_form.fields['query'].widget, TextInput)

class AdvancedSearchFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.advanced_search_form = AdvancedSearchForm()
        return super().setUpTestData()
    
    def test_advanced_search_form_fields(self):
        '''
            Test if AdvancedSearchForm form class use the right
            form fields (price_start, price_end, currency, 
            address, date_start, date_end, categories)
        '''

        form_fields_dict = {'query': '', 'price_start': '', 'price_end': '', 'currency': '', 'address': '', 'date_start': '', 'date_end': '', 'categories': ''}        

        self.assertEqual(self.advanced_search_form.fields.keys(), form_fields_dict.keys())

    def test_advanced_search_form_price_start_field_class(self):
        '''
            Test if price_start field use the right class (IntegerField)
        '''

        self.assertEqual(self.advanced_search_form.fields['price_start'].__class__, IntegerField)

    def test_advanced_search_form_price_start_field_required(self):
        '''
            Test if price_start field has required parameter set to False.
        '''

        self.assertFalse(self.advanced_search_form.fields['price_start'].required)

    def test_advanced_search_form_price_start_field_widget(self):
        '''
            Test if price_start field use the right widget class (NumberInput)
        '''

        self.assertEqual(self.advanced_search_form.fields['price_start'].widget.__class__, NumberInput)

    def test_advanced_search_form_price_end_field_class(self):
        '''
            Test if price_end field use the right class (IntegerField)
        '''

        self.assertEqual(self.advanced_search_form.fields['price_end'].__class__, IntegerField)

    def test_advanced_search_form_price_end_field_required(self):
        '''
            Test if price_end field has the required parameter set to False
        '''

        self.assertFalse(self.advanced_search_form.fields['price_end'].required)

    def test_advanced_search_form_price_end_field_widget(self):
        '''
            Test if price_end field use the right widget class (NumberInput)
        '''

        self.assertEqual(self.advanced_search_form.fields['price_end'].widget.__class__, NumberInput)

    def test_advanced_search_form_currency_class(self):
        '''
            Test if currency field use the right class (ModelMultipleChoiceField)
        '''

        self.assertEqual(self.advanced_search_form.fields['currency'].__class__, ModelMultipleChoiceField)

    def test_advanced_search_form_currency_required(self):
        '''
            Test if currency field has the required parameter set to False
        '''

        self.assertFalse(self.advanced_search_form.fields['currency'].required, False)

    def test_advanced_search_form_currency_queryset(self):
        '''
            Test if currency field has the queryset parameter set to Currency.objects.all()
        '''
        
        self.assertQuerysetEqual(self.advanced_search_form.fields['currency'].queryset, Currency.objects.all())

    def test_advanced_search_form_currency_widget(self):
        '''
            Test if currency field use the right widget class (SelectMultiple)
        '''

        self.assertEqual(self.advanced_search_form.fields['currency'].widget.__class__, SelectMultiple)

    def test_advanced_search_form_address_class(self):
        '''
            Test if address field use the right class (CharField)
        '''

        self.assertEqual(self.advanced_search_form.fields['address'].__class__, CharField)

    def test_advanced_search_form_address_required(self):
        '''
            Test if address field has the required parameter set to False
        '''

        self.assertFalse(self.advanced_search_form.fields['address'].required)

    def test_advanced_search_form_address_widget(self):
        '''
            Test if address field use the right widget (TextInput)
        '''

        self.assertEqual(self.advanced_search_form.fields['address'].widget.__class__, TextInput)

    def test_advanced_search_form_date_start_class(self):
        '''
            Test if date_start field use the right class (DateField)
        '''

        self.assertEqual(self.advanced_search_form.fields['date_start'].__class__, DateField)

    def test_advanced_search_form_date_start_required(self):
        '''
            Test if date_start field has required parameter set to False
        '''

        self.assertFalse(self.advanced_search_form.fields['date_start'].required)

    def test_advanced_search_form_date_start_widget(self):
        '''
            Test if date_start field use the right widget (DateInput)
        '''

        self.assertEqual(self.advanced_search_form.fields['date_start'].widget.__class__, DateInput)

    def test_advanced_search_form_date_end_class(self):
        '''
            Test if date_end field use the right class (DateField)
        '''

        self.assertEqual(self.advanced_search_form.fields['date_end'].__class__, DateField)

    def test_advanced_search_form_date_end_required(self):
        '''
            Test if date_end field has required parameter set to False
        '''

        self.assertFalse(self.advanced_search_form.fields['date_end'].required)

    def test_advanced_search_form_date_end_widget(self):
        '''
            Test if date_end field use the right widget (DateInput)
        '''

        self.assertEqual(self.advanced_search_form.fields['date_end'].widget.__class__, DateInput)

    def test_advanced_search_form_categories_class(self):
        '''
            Test if categories field use the right class (ModelChoiceField)
        '''

        self.assertEqual(self.advanced_search_form.fields['categories'].__class__, ModelChoiceField)

    def test_advanced_serch_form_categories_required(self):
        '''
            Test if categories field has required parameter set to False
        '''

        self.assertFalse(self.advanced_search_form.fields['categories'].required)

    def test_advanced_search_form_queryset(self):
        '''
            Test if categories field has queryset parameter set to Category.objects.all()
        '''

        self.assertQuerySetEqual(self.advanced_search_form.fields['categories'].queryset, Category.objects.all())

    def test_advanced_search_form_categories_widget(self):
        '''
            Test if categories field use the right widget (Select)
        '''

        self.assertEqual(self.advanced_search_form.fields['categories'].widget.__class__, Select)