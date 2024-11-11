from django.test import TestCase, Client
from ..models import Currency, Category, Ad, Report, Profile
from ..views import CreateCurrency, DetailCurrency, UpdateCurrency, DeleteCurrency, ListCurrency
from ..views import CreateCategory, DetailCategory, UpdateCategory, DeleteCategory, ListCategory
from ..views import CreateAd, DetailAd, UpdateAd, DeleteAd, ListAd
from ..views import CreateReport, DetailReport, UpdateReport, DeleteReport, ListReport
from ..views import DetailProfile, UpdateProfile, UpdateUserProfile
from ..forms import CurrencyForm, CategoryForm, AdForm, ReportForm, AdvancedSearchForm, ProfileForm
from accounts.forms import UserForm, UserAdminForm
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
import datetime
from django.contrib.auth.models import User, Group
from .helpers import get_view_status_code, test_view_test_func

class AuthorizationTest(TestCase):
    '''
        This class encapsulates common code to test views authorization.
    '''

    fixtures = ['bazaar/permissions.json', 'bazaar/groups.json']

    @classmethod
    def setUpTestData(cls) -> None:

        cls.GLOBAL_SUPERUSER_USERNAME = 'alice'
        cls.GLOBAL_SUPERUSER_EMAIL = 'alice@gmail.com'
        cls.PASSWORD = 'BlueBr0wn$'

        cls.BAZAAR_SUPERUSER_USERNAME = 'bob'
        cls.BAZAAR_SUPERUSER_EMAIL = 'bob@gmail.com'

        cls.MODERATOR_USERNAME = 'charlie'
        cls.MODERATOR_EMAIL = 'charlie@gmail.com'

        cls.REGULAR_USERNAME = 'daniel'
        cls.REGULAR_EMAIL = 'daniel@yahoo.com'

        cls.superauser_group = Group.objects.get(name = 'Bazaar Superuser')
        cls.moderator_group = Group.objects.get(name = 'Bazaar Moderator')

        cls.global_superuser = User.objects.create_superuser(cls.GLOBAL_SUPERUSER_USERNAME, cls.GLOBAL_SUPERUSER_EMAIL, cls.PASSWORD)
        cls.global_superuser.save()

        cls.bazaar_superuser = User.objects.create_user(cls.BAZAAR_SUPERUSER_USERNAME, cls.BAZAAR_SUPERUSER_EMAIL, cls.PASSWORD)
        cls.bazaar_superuser.groups.add(cls.superauser_group)
        cls.bazaar_superuser.save()

        cls.moderator = User.objects.create_user(cls.MODERATOR_USERNAME, cls.MODERATOR_EMAIL, cls.PASSWORD)
        cls.moderator.groups.add(cls.moderator_group)
        cls.moderator.save()

        cls.regular_user =  User.objects.create_user(cls.REGULAR_USERNAME, cls.REGULAR_EMAIL, cls.PASSWORD)
        cls.regular_user.save()

        # TODO: If you need, create profiles here.\
        # You don't need to create Profiles, remenber that profiles are created
        # automatically.

class CurrencyTestCase(AuthorizationTest):

    @classmethod
    def setUpTestData(cls) -> None:

        cls.CURRENCY = Currency(name = 'United States Dollar', code = 'USD')
        cls.CURRENCY.save()

        cls.CURRENCY_CREATE_URL = reverse_lazy('bazaar:currency_create')
        cls.CURRENCY_DETAIL_URL = reverse_lazy('bazaar:currency_detail', kwargs = {'pk': cls.CURRENCY.pk})
        cls.CURRENCY_UPDATE_URL = reverse_lazy('bazaar:currency_update', kwargs = {'pk': cls.CURRENCY.pk})
        cls.CURRENCY_DELETE_URL = reverse_lazy('bazaar:currency_delete', kwargs = {'pk': cls.CURRENCY.pk})
        cls.CURRENCY_LIST_URL = reverse_lazy('bazaar:currency_list')

        return super().setUpTestData()
    
    def test_create_currency_view_model(self):
        '''
            Test if CreateCurrency view use the correct model (Currency).
        '''

        self.assertEqual(CreateCurrency.model, Currency)

    def test_create_currency_view_form_class(self):
        '''
            Test if CreateCurrency view use the correct form (CurrencyForm).
        '''

        self.assertEqual(CreateCurrency.form_class, CurrencyForm)
    
    def test_create_currency_view_success_url(self):
        '''
            Test if CreateCurrency view redirect to currency:list url.
        '''
        
        self.assertEqual(CreateCurrency.success_url, self.CURRENCY_LIST_URL)

    def test_create_currency_test_func(self):
        '''
            Test if CreateCurrency view has the right implementation of test_func method:
            - When Global Superuser make request, the status code is 200.
            - When Superuser user make request, the status code is 200.
            - When Moderator user make request, the status code is 403.
            - When Regular user make request, the status code is 403.
        '''

        self.client.login(username = self.GLOBAL_SUPERUSER_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_CREATE_URL)
        self.assertEqual(response.status_code, 200)

        self.client.login(username = self.BAZAAR_SUPERUSER_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username = self.MODERATOR_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_CREATE_URL)
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        
        self.client.login(username = self.REGULAR_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_CREATE_URL)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_detail_currency_view_model(self):
        '''
            Test if CurrencyDetail view use the correct model
        '''

        self.assertEqual(DetailCurrency.model, Currency)

    def test_detail_currency_test_func(self):
        '''
            Test if DetailCurrency view has the right implementation of test_func method:
                - When Global Superadmin user make request, the DetailCurrency view return 200 code.
                - When Bazaar Superadmin user make request, the DetailCurrency view return 200 code.
                - When Moderator user make request, the DetailCurrency view return 403 code.
                - When Regular user make request, the DetailCurrency view return 403 code.
        '''

        self.client.login(username = self.GLOBAL_SUPERUSER_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

        self.client.login(username = self.BAZAAR_SUPERUSER_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

        self.client.login(username = self.MODERATOR_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_DETAIL_URL)
        self.assertEqual(response.status_code, 403)

        self.client.login(username = self.REGULAR_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_DETAIL_URL)
        self.assertEqual(response.status_code, 403)

    def test_update_currency_view_model(self):
        '''
            Test if UpdateCurrency view use the correct model (Currency).
        '''

        self.assertEqual(UpdateCurrency.model, Currency)

    def test_update_currency_view_form_class(self):
        '''
            Test if UpdateCurrency view use the correct form class (CurrencyForm)
        '''

        self.assertEqual(UpdateCurrency.form_class, CurrencyForm)
    
    def test_update_currency_view_success_url(self):
        '''
            Test if UpdateCurrency view redirect to bazaar:currency url
        '''

        self.assertEqual(UpdateCurrency.success_url, self.CURRENCY_LIST_URL)

    def test_update_currency_test_func(self):
        '''
            Test if UpdateCurrency view has the right implementation of test_func method:
                - If Global Superadmin user make request, UpdateCurrency view return 200 status code.
                - If Bazaar Superadmin user make request, UpdateCurrency view return 200 status code.
                - If Moderator user make request, UpdateCurrency view return 403 status code.
                - If Regular user make request, UpdateCurrency view return 403 status code.
        '''

        self.client.login(username = self.GLOBAL_SUPERUSER_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

        self.client.login(username = self.BAZAAR_SUPERUSER_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

        self.client.login(username = self.MODERATOR_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_UPDATE_URL)
        self.assertEqual(response.status_code, 403)

        self.client.login(username = self.REGULAR_USERNAME, password = self.PASSWORD)
        response = self.client.get(self.CURRENCY_UPDATE_URL)
        self.assertEqual(response.status_code, 403)

    def test_delete_currency_view_model(self):
        '''
            Test if DeleteCurrency view use the correct model (Currency)
        '''

        self.assertEqual(DeleteCurrency.model, Currency)

    def test_delete_currency_view_success_url(self):
        '''
            Test if DeleteCurrency view redirect to bazaar:list url
        '''

        self.assertEqual(DeleteCurrency.success_url, self.CURRENCY_LIST_URL)

    def test_delete_currency_test_func(self):
        '''
            Test if DeleteCurrency has the right implementation of test_func method:
                - If Global Superadmin user make a request, DeleteCurrency view return 200 status code.
                - If Bazaar Superadmin user make a request, DeleteCurrency view return 200 status code.
                - If Moderator user make a request, DeleteCurrency view return 403 status code.
                - If Regular user make a request, DeleteCurrency view return 403 status code.
        '''

        self.assertEqual(get_view_status_code(self.client, self.CURRENCY_DELETE_URL, self.GLOBAL_SUPERUSER_USERNAME, self.PASSWORD), 200)
        self.assertEqual(get_view_status_code(self.client, self.CURRENCY_DELETE_URL, self.BAZAAR_SUPERUSER_USERNAME, self.PASSWORD), 200)
        self.assertEqual(get_view_status_code(self.client, self.CURRENCY_DELETE_URL, self.MODERATOR_USERNAME, self.PASSWORD), 403)
        self.assertEqual(get_view_status_code(self.client, self.CURRENCY_DELETE_URL, self.REGULAR_USERNAME, self.PASSWORD), 403)
        

    def test_list_currency_view_model(self):
        '''
            Test if ListCurrency view use the correct model (Currency).
        '''
        
        self.assertEqual(ListCurrency.model, Currency)

    def test_list_currency_test_func(self):
        '''
            Test if ListCurrency view has the right implementation of test_func method:

            - If Global Superuser user make a request, ListCurrency view return 200 status code.
            - If Bazaar Superuser user make a request, ListCurrency view return 200 status code.
            - If Bazaar Moderator user make a request, ListCurrency view return 403 status code.
            - If Regular user make a request, ListCurrency view return 403 status code. 
        '''

        self.assertEqual(get_view_status_code(self.client, self.CURRENCY_LIST_URL, self.GLOBAL_SUPERUSER_USERNAME, self.PASSWORD), 200)
        self.assertEqual(get_view_status_code(self.client, self.CURRENCY_LIST_URL, self.BAZAAR_SUPERUSER_USERNAME, self.PASSWORD), 200)
        self.assertEqual(get_view_status_code(self.client, self.CURRENCY_LIST_URL, self.MODERATOR_USERNAME, self.PASSWORD), 403)
        self.assertEqual(get_view_status_code(self.client, self.CURRENCY_LIST_URL, self.REGULAR_USERNAME, self.PASSWORD), 403)
    

class CategoryTestCase(AuthorizationTest):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.CATEGORY = Category(name = 'Groceries')
        cls.CATEGORY.save()

        cls.CATEGORY_CREATE_URL = reverse_lazy('bazaar:category_create')
        cls.CATEGORY_DETAIL_URL = reverse_lazy('bazaar:category_detail', kwargs = {'pk': cls.CATEGORY.pk})
        cls.CATEGORY_UPDATE_URL = reverse_lazy('bazaar:category_update', kwargs = {'pk': cls.CATEGORY.pk})
        cls.CATEGORY_DELETE_URL = reverse_lazy('bazaar:category_delete', kwargs = {'pk': cls.CATEGORY.pk})
        cls.CATEGORY_LIST_URL = reverse_lazy('bazaar:category_list')

        return super().setUpTestData()
    
    def test_create_category_model(self):
        '''
            Test if CreateCategory view class has the correct model (Category)
        '''

        self.assertEqual(CreateCategory.model, Category)

    def test_create_category_form_class(self):
        '''
            Test if CreateCategory view class has the correct form class (CategoryForm)
        '''

        self.assertEqual(CreateCategory.form_class, CategoryForm)

    def test_create_category_success_url(self):
        '''
            Test if CreateCategory view class has the correct success_url property
            (bazaar:category_list)
        '''

        self.assertEqual(CreateCategory.success_url, self.CATEGORY_LIST_URL)

    def test_create_category_test_func(self):
        '''
            Test if CreateCategory view class has the right implementation of test_func
            method:

            - If Global Superadmin user make a request, CreateCategory view return 200 status code.
            - If Bazaar Superadmin user make a request, CreateCategory view return 200 status code.
            - If Bazaar Moderator user make a request, CreateCategory view return 403 status code.
            - If Regular user make a request, CreateCategory view return 403 status code.
        '''

        test_view_test_func(self, self.CATEGORY_CREATE_URL)
        

    def test_detail_category_model(self):
        '''
            Test if DetailCategory class has the correct model (Category)            
        '''

        self.assertEqual(DetailCategory.model, Category)

    def test_detail_category_test_func(self):
        '''
            Test if DetailCategory view class has the right implementation of test_func
            method:

            - If Global Superadmin user make a request, DetailCategory view return 200 status code.
            - If Bazaar Superadmin user make a request, DetailCategory view return 200 status code.
            - If Bazaar Moderator user make a request, DetailCategory view return 403 status code.
            - If Regular user make a request, DetailCategory view return 403 status code.
        '''

        test_view_test_func(self, self.CATEGORY_DETAIL_URL)

    def test_update_category_model(self):
        '''
            Test if UpdateCategory class has the correct model (Category)
        '''

        self.assertEqual(UpdateCategory.model, Category)    

    def test_update_category_form_class(self):
        '''
            Test if UpdateCategory class has the correct form_class (CategoryForm)
        '''

        self.assertEqual(UpdateCategory.form_class, CategoryForm)

    def test_update_category_form_success_url(self):
        '''
            Test if UpdateCategory class has the correct success_url property (bazaar:category_list)
        '''

        self.assertEqual(UpdateCategory.success_url, self.CATEGORY_LIST_URL)

    def test_update_category_test_func(self):
        '''
            Test if UpdateCategory view class has the right implementation of test_func method:

            - If Global Superadmin user make a request, UpdateCategory view return 200 status code.
            - If Bazaar Superadmin user make a request, UpdateCategory view return 200 status code.
            - If Bazaar Moderator user make a request, UpdateCategory view return 403 status code.
            - If Regular user make a request, UpdateCategory view return 403 status code.
        '''
        
        test_view_test_func(self, self.CATEGORY_UPDATE_URL)

    def test_delete_category_model(self):
        '''
            Test if DeleteCategory class has the corrrect model property (Category)
        '''

        self.assertEqual(DeleteCategory.model, Category)

    def test_delete_category_success_url(self):
        '''
            Test if DeleteCategory class has the correct success_url property (bazaar:category_list)
        '''

        self.assertEqual(DeleteCategory.success_url, self.CATEGORY_LIST_URL)

    def test_delete_category_test_func(self):
        '''
            Test if DeleteCategory view class has the right implementation of test_func method:

            - If Global Superadmin user make a request, DeleteCategory view return 200 status code.
            - If Bazaar Superadmin user make a request, DeleteCategory view return 200 status code.
            - If Bazaar Moderator user make a request, DeleteCategory view return 403 status code.
            - If Regular user make a request, DeleteCategory view return 403 status code.
        '''

        test_view_test_func(self, self.CATEGORY_DELETE_URL)
        

    def test_list_category_model(self):
        '''
            Test if ListCategory class has the correct model property (Category)
        '''

        self.assertEqual(ListCategory.model, Category)

    def test_list_category_test_func(self):
        '''
            Test if ListCategory view class has the right implementation of test_func method:

            - If Global Superadmin user make a request, ListCategory view return 200 status code.
            - If Bazaar Superadmin user make a request, ListCategory view return 200 status code.
            - If Bazaar Moderator user make a request, ListCategory view return 403 status code.
            - If Regular user make a request, ListCategory view return 403 status code.
        '''

        test_view_test_func(self, self.CATEGORY_LIST_URL)

class AdTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        # To create an Ad, you need create first:
        # Currency
        # Category
        # User ?
        cls.CURRENCY = Currency(name = 'United States Dollar', code = 'USD')        
        cls.CURRENCY.save()

        cls.CATEGORY = Category(name = 'Grocery')
        cls.CATEGORY.save()

        cls.USER = User(username = 'Manolo', password = 'Password')
        cls.USER.save()

        cls.AD = Ad(
            title = 'I sell cucumbers', 
            description = 'I have some fresh cucumbers. You can buy it.',
            price = 10,
            ) # TODO: Complete this setUpTestData
        cls.AD.save()

        cls.AD_CREATE_URL = reverse_lazy('bazaar:ad_create')
        cls.AD_DETAIL_URL = reverse_lazy('bazaar:ad_detail', kwargs = {'pk': {}})
        cls.AD_LIST_URL = reverse_lazy('bazaar:ad_list')

        return super().setUpTestData()
    
    def test_create_ad_model(self):
        '''
            Test if CreateAd class use the correct model (Ad)
        '''

        self.assertEqual(CreateAd.model, Ad)

    def test_create_ad_form_class(self):
        '''
            Test if CreateAd class use the correct form_class (AdForm)
        '''

        self.assertEqual(CreateAd.form_class, AdForm)

    def test_create_ad_success_url(self):
        '''
            Test if CreateAd class use the correct success_url property (reverse('bazaar:ad_list'))
        '''

        self.assertEqual(CreateAd.success_url, self.AD_LIST_URL)

    def test_detail_ad_model(self):
        '''
            Test if DetailAd class use the correct model property (Ad)
        '''

        self.assertEqual(DetailAd.model, Ad)

    def test_update_ad_model(self):
        '''
            Test if UpdateAd class use the correct model property (Ad)
        '''

        self.assertEqual(UpdateAd.model, Ad)

    def test_update_ad_form_class(self):
        '''
            Test if UpdateAd class use the correct form_class property (AdForm)
        '''

        self.assertEqual(UpdateAd.form_class, AdForm)

    def test_update_ad_success_url(self):
        '''
            Test if UpdateAd class use the correct success_url property (reverse(bazaar:ad_list))
        '''

        self.assertEqual(UpdateAd.success_url, self.AD_LIST_URL)

    def test_delete_ad_model(self):
        '''
            Test if DeleteAd class use the correct model property (Ad)
        '''

        self.assertEqual(DeleteAd.model, Ad)

    def test_delete_ad_success_url(self):
        '''
            Test if DeleteAd class use the correct success_url property (reverse('bazaar:ad_list'))
        '''

        self.assertEqual(DeleteAd.success_url, self.AD_LIST_URL)

    def test_list_ad_model(self):
        '''
            Test if ListAd class use the correct model property (Ad)
        '''

        self.assertEqual(DeleteAd.model, Ad)

    def test_list_ad_model_get_queryset(self):
        '''
            Test if ListAd class have a correct implementation of get_queryset
            method. This method filter ads, using GET parameters.
        '''

        '''
         create a group of keywords
         use the keywords to create a ad (ad_with_keywords)        
         create an ad without keywords (ad_without_keywords)
         search ads using the keywords.
         check if the returned ad is ad_with_keyword
        '''
        
        dollar = Currency(name='United States Dollar', code='USD')
        dollar.save()

        euro = Currency(name='European Union Currency', code='EUR')
        euro.save()

        yen = Currency(name='Japanese Yen', code='JPY')
        yen.save()
        
        electronic = Category(name='Electronic', priority = 1)
        electronic.save()
        
        key = 'smartphone'
        description = 'snapdragon'
        currency = dollar
        address = 'Ice town, Antartida'
        alternative_currency_1 = euro
        alternative_currency_2 = yen
        category = electronic

        ad_with_keywords = Ad(
            title = f'I sell {key}',
            description = f'This {key} has {description}',
            price = 90,
            currency = currency,
            address = f'{address}. Number 12345',
            date = datetime.date(2005, 1, 1),
            category = category
        )

        ad_with_keywords.save()
        ad_with_keywords.alternative_currencies.add(alternative_currency_1)
        ad_with_keywords.alternative_currencies.add(alternative_currency_2)
        ad_with_keywords.save()

        bitcoin = Currency(name='Bitcoin', code='BTC')
        bitcoin.save()
        litecoin = Currency(name='Litecoin', code='LTC')
        litecoin.save()
        bitcoin_cash = Currency(name='Bitcoin Cash', code='BCH')
        bitcoin_cash.save()
        cloths = Category(name='Cloths', priority = 2)
        cloths.save()

        ad_without_keywords = Ad(
            title = 'I sell clothes',
            description = 'I have several sizes and colors of t-shirts',
            price = 150,
            currency = bitcoin,
            address = 'Frozen neighborhood, Artic',
            date = datetime.date(2022, 1, 1),
            category = cloths
        )

        ad_without_keywords.save()
        ad_without_keywords.alternative_currencies.add(litecoin)
        ad_without_keywords.alternative_currencies.add(bitcoin_cash)
        ad_without_keywords.save()
        
        query_strings = {
            'query': key,
            'currencies': [currency.pk, alternative_currency_1.pk, alternative_currency_2.pk],
            'address': address,
            'category': category.pk
            }
        
        for key, value in query_strings.items():
            response = self.client.get(reverse_lazy('bazaar:ad_list'), {key: value})            
            self.assertEqual(response.context['object_list'].get(), ad_with_keywords)
            
        query_strings = {
            'price': (50, 100), 
            'date': (datetime.date(2000,1, 1), datetime.date(2010, 1, 1))
            }
        
        for key, range in query_strings.items():
            # Create a query using a range
            response = self.client.get(reverse_lazy('bazaar:ad_list'), {f'{key}_start': range[0], f'{key}_end': range[1]})
            
            self.assertEqual(response.context['object_list'].get(), ad_with_keywords)

    def test_list_ad_get_context_data(self):
        '''
            Test if ListAd view has advanced_search_form on the context
            and if this value is instance of AdvancedSearchForm class.
        '''

        response = self.client.get(reverse_lazy('bazaar:ad_list'))
        
        self.assertIsInstance(response.context.get('advanced_search_form'), AdvancedSearchForm)

class ReportTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        cls.dollar = Currency(name='United States Dollar', code='USD')
        cls.litecoin = Currency(name='Litecoin', code='LTC')
        cls.dollar.save()
        cls.litecoin.save()

        # cls.generator = Generator()
        # cls.category_group = cls.generator.create_category_group_model()

        cls.smartphones = Category(name = 'Smartphones', priority = 1)
        cls.smartphones.save()

        cls.ad = Ad(
            title = 'Cheap robbed smartphone',
            description = '''I sell this robbed smartphone, only on 25$. Hurry 
                up! I have more! You can contact me using my anonymous mail 
                address smartphonetheft@dark.com or you can see me on the dark..''',
            price = 25,
            currency = cls.dollar,
            address = 'Underground Bridge, Atlantis',
            name = 'John Doe',
            phone = '',
            mail = 'smartphonetheft@dark.com',
            category = cls.smartphones
        )
        cls.ad.save()
        cls.ad.alternative_currencies.set([cls.litecoin])

        cls.report = Report()
                
        cls.LIST_REPORT_URL = reverse_lazy('bazaar:report_list')

        cls.client = Client()

        return super().setUpTestData()
    
    def test_create_report_model(self):
        '''
            Test if CreateReport view has the correct model property (Report)
        '''

        self.assertEqual(CreateReport.model, Report)

    def test_create_report_form_class(self):
        '''
            Test if CreateReport view has the correct form_class property (ReportForm)
        '''

        self.assertEqual(CreateReport.form_class, ReportForm)

    def test_create_report_success_url(self):
        '''
            Test if CreateReport view has the correct success_url property (bazaar:report_list)
        '''

        self.assertEqual(CreateReport.success_url, self.LIST_REPORT_URL)

    def test_create_report_get_initial(self):
        '''
            Test if CreateReport view has implemented sucessfully
            get_initial method. If this is true, view return a ad_pk
            on the content.
        '''

        ad_pk = 19
        response = self.client.get(reverse_lazy('bazaar:report_create', kwargs={'pk': ad_pk}))
        
        self.assertContains(response, f'value="{ad_pk}"')

    def test_detail_report_model(self):
        '''
            Test if DetailReport view has the correct model property (Report)
        '''

        self.assertEqual(DetailReport.model, Report)

    def test_update_report_model(self):
        '''
            Test if UpdateReport view has the correct model property (Report)
        '''

        self.assertEqual(UpdateReport.model, Report)

    def test_update_report_form_class(self):
        '''
            Test if UpdateReport view has the correct form_class property (ReportForm)
        '''

        self.assertEqual(UpdateReport.form_class, ReportForm)

    def test_update_report_success_url(self):
        '''
            Test if UpdateReport view has the correct success_url property (bazaar:report_list)
        '''

        self.assertEqual(UpdateReport.success_url, self.LIST_REPORT_URL)

    def test_delete_report_model(self):
        '''
            Test if DeleteReport view has the correct model property (Report)
        '''

        self.assertEqual(DeleteReport.model, Report)

    def test_delete_report_success_url(self):
        '''
            Test if DeleteReport view has the correct success_url property(bazaar:report_list)
        '''

        self.assertEqual(DeleteReport.success_url, self.LIST_REPORT_URL)

    def test_list_report_model(self):
        '''
            Test if ListReport view has the correct model property (Report)
        '''

        self.assertEqual(ListReport.model, Report)

class ProfileTestCase(AuthorizationTest):
    
    def test_detail_profile_model(self):
        '''
            Test if DetailProfile view has the right model property (Profile)
        '''
        self.assertEqual(DetailProfile.model, Profile)

    def test_detail_profile_get_object(self):
        '''
            Test if DetailProfile view implements
            successfully get_object method (This method
            return the Profile object associated with the User
            that make the request)
        '''

        self.client.login(username = self.REGULAR_USERNAME, password = self.PASSWORD)
        response = self.client.get(reverse_lazy('bazaar:profile_detail'))
        self.assertEqual(response.context['object'], self.regular_user.profile)

    def test_update_profile_model(self):
        '''
            Test if UpdateProfile view has the right model property (Profile)
        '''

        self.assertEqual(UpdateProfile.model, Profile)

    def test_update_profile_form_class(self):
        '''
            Test if UpdateProfile view has the right form_class property (ProfileForm)
        '''

        self.assertEqual(UpdateProfile.form_class, ProfileForm)

    def test_update_profile_success_url(self):
        '''
            Test if UpdateProfile view has the right success_url property(reverse_lazy('bazaar:profile_detail'))
        '''

        self.assertEqual(UpdateProfile.success_url, reverse_lazy('bazaar:profile_detail'))

    def test_update_profile_get_object(self):
        '''
            Test if get_object method return the associated
            profile with the user that make the request
        '''

        self.client.login(username = self.REGULAR_USERNAME, password = self.PASSWORD)
        response = self.client.get(reverse_lazy('bazaar:profile_update'))
        
        self.assertEqual(response.context['object'], self.regular_user.profile)

    def test_update_profile_get_context_data(self):
        '''
            Test if UpdateProfile view has the right implementation of 
            get_context_data method. This method should return on context the
            following data:

            user_form: UserAdminForm | UserForm Return UserAdminForm if user is superadmin
            UserForm otherwise
            password_form: PasswordChangeForm
        '''

        self.client.login(username = self.REGULAR_USERNAME, password = self.PASSWORD)
        response = self.client.get(reverse_lazy('bazaar:profile_update'))
        self.assertIsInstance(response.context['user_form'], UserForm)
        self.assertIsInstance(response.context['password_form'], PasswordChangeForm)

        self.client.login(username = self.BAZAAR_SUPERUSER_USERNAME, password = self.PASSWORD)
        response = self.client.get(reverse_lazy('bazaar:profile_update'))
        self.assertIsInstance(response.context['user_form'], UserAdminForm)

class UserTestCase(TestCase):

    def test_update_user_profile_success_url(self):
        '''
            Test if UpdateProfile view has the right success_url property (reverse_lazy('bazaar:profile_detail'))
        '''

        self.assertEqual(UpdateUserProfile.success_url, reverse_lazy('bazaar:profile_detail'))




