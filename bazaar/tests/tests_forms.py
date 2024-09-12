from django.test import TestCase
from ..forms import CurrencyForm, CategoryForm, AdForm, ReportForm, SimpleSearchForm, AdvancedSearchForm
from ..models import Currency, Category, Ad, Report
from django.forms.widgets import TextInput, Textarea, NumberInput, Select, EmailInput, SelectMultiple, ClearableFileInput, HiddenInput

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
        simple_search_form = SimpleSearchForm()
        return super().setUpTestData()

    def test_simple_search_form_fields(self):
        '''
            Test if SimpleSearchForm form class has the correct fields
            (query)
        '''

        simple_search_form = SimpleSearchForm()

        self.assertIn('query', simple_search_form.fields.keys())

    def test_simple_search_form_query_field_class(self):
        '''
            Test if query form field use the correct class (CharField)
        '''

        