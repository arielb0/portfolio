from django.test import TestCase
from ..models import Currency, Category, Ad, Report, Profile
from django.db.models.fields.related import OneToOneField
from django.db.models.fields import CharField
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from scull_suite.settings import MEDIA_ROOT, STATICFILES_DIRS
import shutil
import os
from bazaar.tests.helpers import Generator

# Create your tests here.

class CurrencyTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.generator = Generator()
        cls.NAME = 'USD Dollar'
        cls.CODE = 'USD'
        # cls.category_group = cls.generator.create_category_group_model()
        return super().setUpTestData()
    
    def test_name_unique_restriction(self):
        '''
            Test if name property has a unique restriction.
        '''
        currency_1 = Currency(name = self.NAME, code = self.CODE)
        currency_2 = Currency(name = self.NAME, code = 'USD1')
        currency_1.save()

        with self.assertRaises(IntegrityError):
            currency_2.save()

    def test_name_length_restriction(self):
        '''
            Test if name property has length restriction.
        '''
        currency_1 = Currency(name = self.generator.generate_random_string(33))

        with self.assertRaises(ValidationError):
            currency_1.full_clean()

    def test_code_unique_restriction(self):
        '''
            Test if code property has unique restriction
        '''
        currency_1 = Currency(name = self.NAME, code = self.CODE)
        currency_2 = Currency(name = 'USD Dollar2', code = self.CODE)
        currency_1.save()
        with self.assertRaises(IntegrityError):
            currency_2.save()

    def test_code_max_length_restriction(self):
        '''
            Test if code property has max length restriction of 4 characters
        '''
        currency_1 = Currency(name = self.NAME, code = 'USDXX')

        with self.assertRaises(ValidationError):
            currency_1.full_clean()

class CategoryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.NAME = 'Books'        
        cls.PICTURE = f'{STATICFILES_DIRS[0]}/img/grocery.webp'
        cls.OLD_PICTURE = f'{MEDIA_ROOT}/images/categories/grocery.webp'
        cls.NEW_PICTURE = f'{MEDIA_ROOT}/images/categories/grocery_1.webp'

        return super().setUpTestData()
    
    def test_name_unique_restriction(self):
        '''
            Test if name property has unique restriction
        '''
        category_1 = Category(name = self.NAME, priority = 1)
        category_2 = Category(name = self.NAME, priority = 2)
        category_1.save()

        with self.assertRaises(IntegrityError):
            category_2.save()

    def test_picture_upload_to(self):
        '''
            Test if picture property has upload_to parameter with the right value ('images/categories')
        '''

        self.assertEqual(Category.picture.field.upload_to, 'images/categories')

    def test_picture_blank(self):
        '''
            Test if picture property has blank parameter with the right value (True)
        '''

        self.assertEqual(Category.picture.field.blank, True)

    def test_picture_null(self):
        '''
            Test if picture property has null parameter with the right value (True)
        '''

        self.assertEqual(Category.picture.field.null, True)

    def test_priority_blank(self):
        '''
            Test if priority property has blank parameter with the right value (True)
        '''

        self.assertEqual(Category.picture.field.blank, True)

    def test_priority_null(self):
        '''
            Test if priority property has null parameter with the right value (True)
        '''

        self.assertEqual(Category.picture.field.null, True)

    def test_parent_category_to(self):
        '''
            Test if parent_category property is linked with the right model (Category)
        '''

        self.assertEqual(Category.parent_category.field.related_model, Category)

    def test_parent_category_blank(self):
        '''
            Test if parent_category property has the right value on blank parameter (True)
        '''
        
        self.assertEqual(Category.parent_category.field.blank, True)

    def test_parent_category_null(self):
        '''
            Test if parent_category property has the right value on null parameter (True)
        '''

        self.assertEqual(Category.parent_category.field.null, True)

    def test_delete(self):
        '''
            Test if delete method is correcly implemented
            (When the model is deleted, delete picture)
        '''       

        shutil.copy(self.PICTURE, self.OLD_PICTURE)
        category = Category(name = self.NAME, picture = self.OLD_PICTURE)
        category.save()
        category.delete()
        
        self.assertFalse(os.path.exists(self.OLD_PICTURE))

    def test_save(self):
        '''
            Test if save method is correctly implemented
            (If picture change, delete the old picture)
        '''       

        shutil.copy(self.PICTURE, self.OLD_PICTURE)
        shutil.copy(self.PICTURE, self.NEW_PICTURE)

        category = Category(name = self.NAME, picture = self.OLD_PICTURE)
        category.save()

        category.picture = self.NEW_PICTURE
        category.save()

        self.assertFalse(os.path.exists(self.OLD_PICTURE))

        category.delete()

class AdTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        cls.generator = Generator()

        cls.currency_1 = Currency(name = 'US Dollar', code = 'USD')
        cls.currency_1.save()

        cls.currency_2 = Currency(name = 'Cuban Peso', code = 'CUP')
        cls.currency_2.save()

        cls.currency_3 = Currency(name = 'Litecoin', code = 'LTC')
        cls.currency_3.save()
        
        cls.category = Category(name = 'Storage devices', priority = 1)
        cls.category.save()

        cls.moderator = User(username = 'Peter', password = 'weak_password_123_321')
        cls.moderator.save()

        cls.owner = cls.generator.create_user_model()

        cls.TITLE = '16GB USB 3.1 ADATA Flash Drive'
        cls.DESCRIPTION = 'I sell this pendrive. It \
        is new. If you are interested, please contact \
        me using the phone number below. Please, I \
        only receive SMS.'
        cls.PRICE = '2.12'
        cls.DATE = '2024-01-01'
        cls.STATUS = '0'
        cls.PICTURE_PATH = f'{MEDIA_ROOT}/images'
        cls.PICTURE_EXTENSION = '.jpg'
        cls.RANK = '1.1'

        return super().setUpTestData()
    
    def test_title_max_length_restriction(self):        
        '''
            Test if title property has a maximum length restriction of 64 characters.
        '''
        # copy a file to another path
        
        ad = Ad(
            title = self.generator.generate_random_string(65),
            description = self.DESCRIPTION,
            price = self.PRICE,
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            rank = self.RANK,
            owner = self.owner
        )

        with self.assertRaises(ValidationError):       
            ad.full_clean()

    def test_description_max_length_restriction(self):
        '''
            Test if description property has maximum length restriction of 254 characters
        '''

        ad = Ad(
            title = self.TITLE,
            description = self.generator.generate_random_string(255),
            price = self.PRICE,
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            rank = self.RANK,
            owner = self.owner
        )

    def test_price_max_digits(self):
        '''
            Test if price property has maximum digits restriction.
        '''

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = self.generator.generate_random_string(11),
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            rank = self.RANK,
            owner = self.owner
        )

        with self.assertRaises(ValidationError):
            ad.full_clean()

    def test_price_max_decimal_places(self):
        '''
            Test if price property has restriction of 2 maximum decimal places.
        '''

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = '1.123',
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            rank = self.RANK,
            owner = self.owner
        )

        with self.assertRaises(ValidationError):
            ad.full_clean()

    def test_currency_non_null(self):
        '''
            Test if currency property has non null restriction.
        '''

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = self.PRICE,            
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            rank = self.RANK,
            owner = self.owner
        )

        with self.assertRaises(ValidationError):
            ad.full_clean()

    def test_date_valid_data(self):
        '''
            Test if date property check if data is valid
        '''

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = self.PRICE,
            currency = self.currency_1,
            date = '2024-31-31',
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            rank = self.RANK,
            owner = self.owner
        )

        with self.assertRaises(ValidationError):
            ad.full_clean()

    # TODO: Include alternative_currencies tests
    # TODO: Include category tests
    # TODO: Include moderator tests

    def test_status_valid_choice(self):
        '''
            Test if status property has a constraint that only allow values between 0 and 2.
        '''

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = self.PRICE,
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = '-1',
            rank = self.RANK,
            owner = self.owner
        )

        with self.assertRaises(ValidationError):
            ad.full_clean()

        ad.status = '3'

        with self.assertRaises(ValidationError):
            ad.full_clean()

    def test_rank_max_digits(self):
        '''
            Test if rank property has maximum length constraint of 10 characters.
        '''

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = self.PRICE,
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            rank = self.generator.generate_random_string(11),
            owner = self.owner
        )

        with self.assertRaises(ValidationError):
            ad.full_clean()

    def test_rank_max_decimal_places(self):
        '''
            Test if rank property has maximum decimal places constraint of 2 characters.
        '''

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = self.PRICE,
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            rank = '1.123',
            owner = self.owner
        )

        with self.assertRaises(ValidationError):
            ad.full_clean()
    
    def test_delete(self):
        '''
            Test if Ad model delete picture files linked using picture_n properties.
        '''
        
        for number in range(0, 10):
            shutil.copyfile(f'{STATICFILES_DIRS[0]}/img/smartphone.jpg', f'{self.PICTURE_PATH}/{number}{self.PICTURE_EXTENSION}')

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = self.PRICE,
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            moderator = self.moderator,
            status = self.STATUS,
            picture_0 = f'{self.PICTURE_PATH}/0{self.PICTURE_EXTENSION}',
            picture_1 = f'{self.PICTURE_PATH}/1{self.PICTURE_EXTENSION}',
            picture_2 = f'{self.PICTURE_PATH}/2{self.PICTURE_EXTENSION}',
            picture_3 = f'{self.PICTURE_PATH}/3{self.PICTURE_EXTENSION}',
            picture_4 = f'{self.PICTURE_PATH}/4{self.PICTURE_EXTENSION}',
            picture_5 = f'{self.PICTURE_PATH}/5{self.PICTURE_EXTENSION}',
            picture_6 = f'{self.PICTURE_PATH}/6{self.PICTURE_EXTENSION}',
            picture_7 = f'{self.PICTURE_PATH}/7{self.PICTURE_EXTENSION}',
            picture_8 = f'{self.PICTURE_PATH}/8{self.PICTURE_EXTENSION}',
            picture_9 = f'{self.PICTURE_PATH}/9{self.PICTURE_EXTENSION}',
            rank = self.RANK,
            owner = self.owner
        )

        ad.save()
        ad.delete()

        for number in range(0, 10):
            self.assertFalse(os.path.exists(f'{self.PICTURE_PATH}/{number}{self.PICTURE_EXTENSION}'))

    def test_save(self):
        '''
            Test if Ad save method deletes old picture_n fields when an Ad is updated
            changing these fields.
        '''

        old_picture_path = f'{self.PICTURE_PATH}/old_picture.jpg'
        new_picture_path = f'{self.PICTURE_PATH}/new_picture.jpg'

        shutil.copyfile(f'{STATICFILES_DIRS[0]}/img/smartphone.jpg', old_picture_path)
        shutil.copyfile(f'{STATICFILES_DIRS[0]}/img/smartphone.jpg', new_picture_path)

        ad = Ad(
            title = self.TITLE,
            description = self.DESCRIPTION,
            price = self.PRICE,
            currency = self.currency_1,
            date = self.DATE,
            category = self.category,
            picture_0 = f'{self.PICTURE_PATH}/old_picture.jpg',
            owner = self.owner
        )

        ad.save()

        ad.picture_0 = f'{self.PICTURE_PATH}/new_picture.jpg'
        ad.save()
        ad.delete()

        self.assertFalse(os.path.exists(old_picture_path))


class ReportTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.generator = Generator()

        currency = Currency(name = 'US Dollar', code = 'USD')
        currency.save()

        # category_group = cls.generator.create_category_group_model()
        cls.owner = cls.generator.create_user_model()
        
        category = Category(name = 'Tools', priority = 1)
        category.save()

        ad = Ad(
            title = 'I sell a weapon to throw stones',
            description = 'If you want to throw stones, buy this weapon..',
            price = '2000',
            currency = currency,
            date = '2024-01-01',
            category = category,
            status = '0',
            rank = '1000',
            owner = cls.owner
        )
        ad.save()

        moderator = User(
            username = 'Peter',
            password = 'weak_password_0687'
        )
        moderator.save()

        cls.REASON = '0'
        cls.DESCRIPTION = 'These ads contains promotions to illegal stuff, like weapon.'
        cls.DATE = '2024-01-02'
        cls.READED = True
        cls.MODERATOR = moderator
        cls.AD = ad
        return super().setUpTestData()
    
    def test_reason_valid_choice(self):
        '''
            Test if reason property has a constraint that only allows values between 0 and 5.
        '''
    
        report = Report(
            reason = '-1',
            description = self.DESCRIPTION,
            date = self.DATE,
            readed = self.READED,
            moderator = self.MODERATOR,
            ad = self.AD
        )

        with self.assertRaises(ValidationError):
            report.full_clean()

        report.reason = '6'

        with self.assertRaises(ValidationError):
            report.full_clean()

    def test_description_max_length(self):
        '''
            Test if description property has maximum length restriction of 255 characters.
        '''
        
        report = Report(
            reason = self.REASON,
            description = self.generator.generate_random_string(255), # Here are a bug! full_clean() method don't show error..            
            date = self.DATE,
            readed = self.READED,
            moderator = self.MODERATOR,
            ad = self.AD
        )

        with self.assertRaises(ValidationError):
            report.full_clean()

    def test_date_valid_data(self):
        '''
            Test if date property check if value is a valid date.
        '''
        
        report = Report(
            reason = self.REASON,
            description = self.DESCRIPTION,
            date = '2024-31-31',
            readed = self.READED,
            moderator = self.MODERATOR,
            ad = self.AD
        )

        with self.assertRaises(ValidationError):
            report.full_clean()

    def test_readed_valid_data(self):
        '''
            Test if readed property check if value is a valid Boolean data.
        '''

        report = Report(
            reason = self.REASON,
            description = self.DESCRIPTION,
            date = self.DATE,
            readed = 'Truee',
            moderator = self.MODERATOR,
            ad = self.AD
        )

        with self.assertRaises(ValidationError):
            report.full_clean()

class ProfileTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        cls.user_field = Profile._meta.get_field('user')
        cls.address_field = Profile._meta.get_field('address')
        cls.phone_field = Profile._meta.get_field('phone')

        return super().setUpTestData()
    
    def test_user_field_type(self):
        '''
            Test if user field use the right field type (OneToOneField)
        '''
        
        self.assertIsInstance(self.user_field, OneToOneField)        
    
    def test_user_related_model(self):
        '''
            Test if user field use the right model (User)
        '''

        self.assertEqual(self.user_field.related_model, User)

    def test_user_on_delete(self):
        '''
            Test if user field has set on_delete property to models.CASCADE
            You need to make this test indirectly.
        '''
        
        temporal_user = User(username = 'Ramiro', password = 'Grocer1es34$')
        temporal_user.save()

        profile = Profile(user = temporal_user)
        profile.save()

        temporal_user.delete()

        self.assertQuerySetEqual(Profile.objects.all(), Profile.objects.none())

    def test_address_field_type(self):
        '''
            Test if address field use the right field type (CharField)
        '''
        
        self.assertIsInstance(self.address_field, CharField)

    def test_address_max_length(self):
        '''
            Test if address field has the max_length parameter set to 64
        '''

        self.assertEqual(self.address_field.max_length, 64)

    def test_address_blank(self):
        '''
            Test if address field has the blank parameter set to True
        '''

        self.assertTrue(self.address_field.blank)

    def test_phone_field_type(self):
        '''
            Test if phone field belongs to the right class (CharField)
        '''

        self.assertIsInstance(self.phone_field, CharField)

    def test_phone_max_length(self):
        '''
            Test if phone field has max_length property set to 16
        '''

        self.assertEqual(self.phone_field.max_length, 16)

    def test_phone_blank(self):
        '''
            Test if phone field has blank property set to True
        '''

        self.assertTrue(self.phone_field.blank)