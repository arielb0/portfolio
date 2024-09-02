from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Currency, Category, Ad, Report
from ..views import CreateCurrency, DetailCurrency, UpdateCurrency, DeleteCurrency, ListCurrency
from ..views import CreateCategory, DetailCategory, UpdateCategory, DeleteCategory, ListCategory
from ..views import CreateAd, DetailAd, UpdateAd, DeleteAd, ListAd
from ..views import CreateReport, DetailReport, UpdateReport, DeleteReport, ListReport
from django.views import View
from typing import Callable
from bazaar.tests.helpers import Generator

class ViewClassUtil():
      '''
        This class has several util methods to interact with view class and make tests.
      '''
      
      @classmethod
      def get_view_function(self, url: str) -> Callable:
            '''
                This method get the view function associated with url.

                Parameters:
                ----------
                url: The url associated with view.

                Returns:
                -------
                Callable: The view function associated with url.
            '''

            resolve_match = resolve(url)

            return resolve_match.func
      
      @classmethod
      def view_function_is_instance_of_class(self, view_function: Callable, view_class: View) -> bool:
            '''
                This method check if view function is an attribute of a view class.

                Parameters:
                -----------
                view_function (Callable): The view function
                view_class (View): The view class

                Returns:
                --------
                bool: True if view function is an attribute of view class.
            '''            

            if hasattr(view_function, 'view_class') and view_function.view_class == view_class:
                return True

class CurrencyURLsTestCase(TestCase):
        '''
            Currency URL Test Suite.
        '''
        
        @classmethod
        def setUpTestData(cls) -> None:
                
                cls.currency = Currency(name = 'US Dollar', code = 'USD')
                cls.currency.save()
                
                cls.CURRENCY_CREATE_URL = reverse('bazaar:currency_create')
                cls.CURRENCY_DETAIL_URL = reverse('bazaar:currency_detail', kwargs={'pk': cls.currency.pk})
                cls.CURRENCY_UPDATE_URL = reverse('bazaar:currency_update', kwargs={'pk': cls.currency.pk})
                cls.CURRENCY_DELETE_URL = reverse('bazaar:currency_delete', kwargs={'pk': cls.currency.pk})
                cls.CURRENCY_LIST_URL = reverse('bazaar:currency_list')

                return super().setUpTestData()

        def test_currency_create_url_path(self):
            '''
                Test if currency_create url return a /bazaar/currency/create path .
            '''
            
            self.assertEqual(reverse('bazaar:currency_create'), '/bazaar/currency/create')

        def test_currency_create_url_view(self):
            '''
                Test if currency_create url is associated with CreateCurrency view.
            '''

            view_function = ViewClassUtil.get_view_function(self.CURRENCY_CREATE_URL)
            self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, CreateCurrency))
        
        def test_currency_detail_url_path(self):
            '''
                Test if currency_detail url return a /bazaar/currency/<int:pk> path .
            '''

            self.assertEqual(reverse('bazaar:currency_detail', kwargs={'pk': self.currency.pk}), f'/bazaar/currency/{self.currency.pk}')

        def test_currency_detail_url_view(self):
            '''
                Test if currency_detail url is associated with DetailCurrency view.
            '''

            view_function = ViewClassUtil.get_view_function(self.CURRENCY_DETAIL_URL)
            self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, DetailCurrency))

        def test_currency_update_url_path(self):
            '''
                Test if currency_update url return a /bazaar/currency/<int:pk>/update path .
            '''

            self.assertEqual(reverse('bazaar:currency_update', kwargs={'pk': self.currency.pk}), f'/bazaar/currency/{self.currency.pk}/update')

        def test_currency_update_url_view(self):
            '''
                Test if currency_update url is associated with UpdateCurrency view.
            '''

            view_function = ViewClassUtil.get_view_function(self.CURRENCY_UPDATE_URL)
            self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, UpdateCurrency))

        def test_currency_delete_url_path(self):
            '''
                Test if currency_delete url return a /bazaar/currency/<int:pk>/delete path .
            '''

            self.assertEqual(reverse('bazaar:currency_delete', kwargs={'pk': self.currency.pk}), f'/bazaar/currency/{self.currency.pk}/delete')

        def test_currency_delete_url_view(self):
            '''
                Test if currency_delete url is associated with DeleteCurrency view.
            '''

            view_function = ViewClassUtil.get_view_function(self.CURRENCY_DELETE_URL)
            self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, DeleteCurrency))

        def test_currency_list_url_path(self):
            '''
                Test if currency_list url return a /bazaar/currency path .
            '''

            self.assertEqual(reverse('bazaar:currency_list'), '/bazaar/currency')

        def test_currency_list_url_view(self):
            '''
                Test if currency_list url is associated with ListCurrency view.
            '''

            view_function = ViewClassUtil.get_view_function(self.CURRENCY_LIST_URL)
            self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, ListCurrency))

class CategoryURLsTestCase(TestCase):
     
    @classmethod
    def setUpTestData(cls) -> None:
        # cls.generator = Generator()

        # cls.category_group = cls.generator.create_category_group_model()

        cls.category = Category(name = 'Laptops', priority = 1)
        cls.category.save()

        cls.CATEGORY_CREATE_URL = reverse('bazaar:category_create')
        cls.CATEGORY_DETAIL_URL = reverse('bazaar:category_detail', kwargs={'pk': cls.category.pk})
        cls.CATEGORY_UPDATE_URL = reverse('bazaar:category_update', kwargs={'pk': cls.category.pk})
        cls.CATEGORY_DELETE_URL = reverse('bazaar:category_delete', kwargs={'pk': cls.category.pk})
        cls.CATEGORY_LIST_URL = reverse('bazaar:category_list')
        
        return super().setUpTestData()
    '''
    @classmethod
    def tearDownClass(cls) -> None:
          cls.category_group.delete()
          return super().tearDownClass()
    '''
    def test_category_create_url_path(self):
         '''
            Test if bazaar:category_create Django url return /bazaar/category/create path.
         '''

         self.assertEqual(self.CATEGORY_CREATE_URL, '/bazaar/category/create')

    def test_category_create_view(self):
         '''
            Test if bazaar:category_create Django url use the correct view (CreateCategory)
         '''

         view_function = ViewClassUtil.get_view_function(self.CATEGORY_CREATE_URL)
         self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, CreateCategory))

    def test_category_detail_url_path(self):
         '''
            Test if bazaar:category_detail Django url return /bazaar/category/<int:pk> path.
         '''

         self.assertEqual(self.CATEGORY_DETAIL_URL, f'/bazaar/category/{self.category.pk}')
         
    def test_category_detail_view(self):
         '''
            Test if bazaar:category_detail Django url use the correct view class (DetailCurrency)
         '''
         
         view_function = ViewClassUtil.get_view_function(self.CATEGORY_DETAIL_URL)
         self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, DetailCategory))

    def test_category_update_url_path(self):
         '''
            Test if bazaar:category_update Django url return the correct path (/bazaar/category/<int:pk>/update)
         '''

         self.assertEqual(self.CATEGORY_UPDATE_URL, f'/bazaar/category/{self.category.pk}/update')

    def test_category_update_view(self):
         '''
            Test if bazaar:category_update Django url use the correct view class (UpdateCategory).
         '''

         view_function = ViewClassUtil.get_view_function(self.CATEGORY_UPDATE_URL)
         self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, UpdateCategory))

    def test_category_delete_url_path(self):
         '''
            Test if bazaar:category_delete Django url pattern return the correct path (/bazaar/category/<int:pk>/delete).
         '''

         self.assertEqual(self.CATEGORY_DELETE_URL, f'/bazaar/category/{self.category.pk}/delete')

    def test_category_delete_view(self):
         '''
            Test if bazaar:category_delete Django url use the correct view class (DeleteCategory)
         '''
         
         view_function = ViewClassUtil.get_view_function(self.CATEGORY_DELETE_URL)
         self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, DeleteCategory))

    def test_category_list_url_path(self):
         '''
            Test if bazaar:category Django url redirect to /bazaar/category path.
         '''

         self.assertEqual(self.CATEGORY_LIST_URL, '/bazaar/category')

    def test_category_list_view(self):
         '''
            Test if bazaar:category Django url use the correct view class (ListCategory).
         '''

         view_function = ViewClassUtil.get_view_function(self.CATEGORY_LIST_URL)
         self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, ListCategory))

class AdURLTestCase(TestCase):
     
     @classmethod
     def setUpTestData(cls) -> None:
         
         # cls.generator = Generator()

         usd_currency = Currency(
              name = 'United States Dollar', 
              code = 'USD'
            )
         usd_currency.save()

         ada_currency = Currency(
              name = 'ADA (Cardano)',
              code = 'ADA'
         )
         ada_currency.save()

         eur_currency = Currency(
              name = 'European currency',
              code = 'EUR'
         )
         eur_currency.save()

         # cls.category_group = cls.generator.create_category_group_model()

         cloths_and_shoes_category = Category(name='Cloths and shoes', priority = 1)
         cloths_and_shoes_category.save()
         
         cls.ad = Ad(
              title='Artisan shoes',
              description='Artisan shoes, good quality',
              price=20,
              currency= usd_currency,
              address='New Economy, 42 Street, New Zeland',
              name='Smith Doe',
              phone='0123456789',
              mail='smithdoe01@yahoo.com',
              category=cloths_and_shoes_category,
              rank=1
         )
         cls.ad.save()
         cls.ad.alternative_currencies.add(ada_currency, eur_currency)

         cls.AD_CREATE_URL = reverse('bazaar:ad_create')
         cls.AD_DETAIL_URL = reverse('bazaar:ad_detail', kwargs={'pk': cls.ad.pk})
         cls.AD_UPDATE_URL = reverse('bazaar:ad_update', kwargs={'pk': cls.ad.pk})
         cls.AD_DELETE_URL = reverse('bazaar:ad_delete', kwargs={'pk': cls.ad.pk})
         cls.AD_LIST_URL = reverse('bazaar:ad_list')

         return super().setUpTestData()
     '''
     @classmethod
     def tearDownClass(cls) -> None:
          cls.category_group.delete()
          return super().tearDownClass()
     '''
     
     def test_ad_create_url_path(self):
          '''
            Test if bazaar:ad_create Django url return '/bazaar/create' path.
          '''

          self.assertEqual(self.AD_CREATE_URL, '/bazaar/create')

     def test_ad_create_url_view(self):
          '''
            Test if bazaar:ad_create Django url use the correct view (CreateAd)
          '''

          view_function = ViewClassUtil.get_view_function(self.AD_CREATE_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, CreateAd))

     def test_ad_detail_url_path(self):
          '''
            Test if bazaar:ad_detail Django url return /bazaar/<int:pk> path
          '''

          self.assertEqual(self.AD_DETAIL_URL, f'/bazaar/{self.ad.pk}')

     def test_ad_detail_view(self):
          '''
            Test if bazaar:ad_detail Django path use the correct view class (DetailAd)
          '''

          view_function = ViewClassUtil.get_view_function(self.AD_DETAIL_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, DetailAd))

     def test_ad_update_url_path(self):
          '''
            Test if bazaar:ad_update Django url return /bazaar/<int:pk>/update path
          '''

          self.assertEqual(self.AD_UPDATE_URL, f'/bazaar/{self.ad.pk}/update')

     def test_ad_update_view(self):
          '''
            Test if bazaar:ad_update Django url use the correct view class (UpdateAd)
          '''

          view_function = ViewClassUtil.get_view_function(self.AD_UPDATE_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, UpdateAd))

     def test_ad_delete_url_path(self):
         '''
            Test if bazaar:ad_delete Django url return /bazaar/<int:pk>/delete path
         '''

         self.assertTrue(self.AD_DELETE_URL, f'/bazaar/{self.ad.pk}/delete')

     def test_ad_delete_view(self):
          '''
            Test if bazaar:ad_delete Django url use the correct view class (DeleteView)
          '''

          view_function = ViewClassUtil.get_view_function(self.AD_DELETE_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, DeleteAd))

     def test_ad_list_url_path(self):
          '''
            Test if bazaar:ad_list Django url return /bazaar
          '''

          self.assertTrue(self.AD_LIST_URL, '/bazaar')

     def test_ad_list_view(self):
          '''
            Test if bazaar:ad_list Django url use the correct view class (ListAd)
          '''

          view_function = ViewClassUtil.get_view_function(self.AD_LIST_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view_function, ListAd))
      
class ReportURLTestCase(TestCase):
     
     @classmethod
     def setUpTestData(cls) -> None:
         
         usd = Currency(name='United States Dollar', code='USD')
         usd.save()
         
         # generator = Generator()
         # cls.category_group = generator.create_category_group_model()
         smartphones = Category(name = 'smartphones', priority = 1)
         smartphones.save()

         ad = Ad(
            title = 'Offensive title',
            description = 'Here are a offensive description',  
            price = 1000,
            currency = usd,
            address = 'Moon City, Nowhere',
            name = 'Jordan',
            phone = '',
            mail = 'jordanbatusto@gmail.com',
            category = smartphones
         )
         ad.save()

         cls.report = Report(
              reason = 1,
              description = 'This add is offensive',
              ad = ad,
         )
         cls.report.save()

         cls.REPORT_CREATE_URL = reverse('bazaar:report_create', kwargs={'pk': ad.pk})
         cls.REPORT_DETAIL_URL = reverse('bazaar:report_detail', kwargs={'pk': cls.report.pk})
         cls.REPORT_UPDATE_URL = reverse('bazaar:report_update', kwargs={'pk': cls.report.pk})
         cls.REPORT_DELETE_URL = reverse('bazaar:report_delete', kwargs={'pk': cls.report.pk})
         cls.REPORT_LIST_URL = reverse('bazaar:report_list')

         return super().setUpTestData()
     '''
     @classmethod
     def tearDownClass(cls) -> None:
          cls.category_group.delete()
          return super().tearDownClass()
     '''
    
     def test_report_create_url_path(self):
         '''
            Test if bazaar:report_create Django url has the correct path (/bazaar/report/create)
         '''

         self.assertEqual(self.REPORT_CREATE_URL, '/bazaar/report/create/ad/1')

     def test_report_create_view(self):
         '''
            Test if bazaar:report_create Django url use the correct view class (CreateReport)
         '''

         view = ViewClassUtil.get_view_function(self.REPORT_CREATE_URL)
         self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view, CreateReport))

     def test_report_detail_url_path(self):
          '''
            Test if bazaar:report_detail Django url return the correct path (/bazaar/report/<int:pk>)
          '''

          self.assertEqual(self.REPORT_DETAIL_URL, f'/bazaar/report/{self.report.pk}')

     def test_report_detail_view(self):
          '''
            Test if bazaar:report_detail Django url use the correct view class (ReportDetail).
          '''

          view = ViewClassUtil.get_view_function(self.REPORT_DETAIL_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view, DetailReport))
     
     def test_report_update_url_path(self):
          '''
            Test if bazaar:report_update Django url return the correct path(/bazaar/report/<int:pk>/update)
          '''

          self.assertEqual(self.REPORT_UPDATE_URL, f'/bazaar/report/{self.report.pk}/update')

     def test_report_update_url_view(self):
          '''
            Test if bazaar:report_update Django url use the correct view class (UpdateReport)
          '''

          view = ViewClassUtil.get_view_function(self.REPORT_UPDATE_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view, UpdateReport))

     def test_report_delete_url_path(self):
          '''
            Test if bazaar:report_delete Django url return the correct path (/bazaar/report/<int:pk>/delete)
          '''

          self.assertEqual(self.REPORT_DELETE_URL, f'/bazaar/report/{self.report.pk}/delete')

     def test_report_delete_view(self):
          '''
            Test if bazaar:report_delete Django url use the correct view (DeleteReport)
          '''

          view = ViewClassUtil.get_view_function(self.REPORT_DELETE_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view, DeleteReport))

     def test_report_list_url_path(self):
          '''
            Test if bazaar:report_list Django url return the correct url path (/bazaar/report)
          '''

          self.assertTrue(self.REPORT_LIST_URL, '/bazaar/report')

     def test_report_list_view(self):
          '''
            Test if bazaar:report_list Django url use the correct 
          '''

          view = ViewClassUtil.get_view_function(self.REPORT_LIST_URL)
          self.assertTrue(ViewClassUtil.view_function_is_instance_of_class(view, ListReport))
     