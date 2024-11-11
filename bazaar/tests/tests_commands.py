from django.test import TestCase
from bazaar.models import Currency, Category, Ad
import datetime
from datetime import timedelta
from django.core.management import call_command
from scull_suite.settings import BASE_DIR
import os
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import ObjectDoesNotExist

class CommandsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        # generator = Generator()
        # cls.category_group = generator.create_category_group_model()
        return super().setUpTestData()
    
    def test_delete_old_ads(self):
        '''
            Test if delete_old_ads admin command delete ads older than one month.
        '''

        usd = Currency(name='United States Dollar', code='USD')
        usd.save()

        electronics = Category(name='Electronics', priority = 1)
        electronics.save()
        
        description = 'I have this laptop..'
        price = 500
        address = 'Atlantis City, Australia'
        name = 'Peter'
        phone = '0123456789'
        mail = 'peter67@terra.com'
        actual_date = datetime.datetime.now()
        category = electronics

        actual_ad = Ad(
            title = 'I sell updated chinese laptop',
            description = description,
            price = price,
            currency = usd,
            address = address,
            name = name,
            phone = phone,
            mail = mail,
            date = actual_date,
            category = category,
        )
        actual_ad.save()

        old_ad = Ad(
            title = 'I sell old chinese laptop',
            description = description,
            price = price,
            currency = usd,
            address = address,
            name = name,
            phone = phone,
            mail = mail,
            date = actual_date - timedelta(days = 31),
            category = category,
        )
        old_ad.save()

        call_command('delete_old_ads')

        self.assertQuerySetEqual(Ad.objects.all(), Ad.objects.filter(pk=actual_ad.pk))

    def test_bazaar_makefixtures(self):
        '''
            Test if makefixtures command generate permissions.json and groups.json
            with the right content.
        '''

        '''
            If bazaar/{groups.json, permissions.json} exists, delete it.
            Execute makefixtures command.
            Check if bazaar/{groups.json, permissions.json} exists.
            Check if 'Bazaar Moderator' and 'Bazaar Superuser' has the right permissions.
        '''

        permissions_fixture_path = f'{BASE_DIR}/bazaar/fixtures/bazaar/permissions.json'
        groups_fixture_path = f'{BASE_DIR}/bazaar/fixtures/bazaar/groups.json'

        if os.path.exists(permissions_fixture_path):
            os.remove(permissions_fixture_path)

        if os.path.exists(groups_fixture_path):
            os.remove(groups_fixture_path)

        call_command('bazaar_makefixtures')

        self.assertTrue(os.path.exists(permissions_fixture_path))
        self.assertTrue(os.path.exists(groups_fixture_path))

        try:
            bazaar_moderator = Group.objects.get(name = 'Bazaar Moderator')            
        except ObjectDoesNotExist:
            self.fail('Bazaar Moderator group does not exist on database')

        try:
            bazaar_superuser = Group.objects.get(name = 'Bazaar Superuser')
        except ObjectDoesNotExist:
            self.fail('Bazaar Superadmin group does not exist on database')

        bazaar_moderator_permissions = bazaar_moderator.permissions.all().values_list('codename', flat = True)
        bazaar_superuser_permissions = bazaar_superuser.permissions.all().values_list('codename', flat = True)

        self.assertIn('delete_ad', bazaar_moderator_permissions)
        self.assertIn('view_report', bazaar_moderator_permissions)

        for model in ['currency', 'category', 'ad', 'report', 'user']:
            if model != 'ad':
                self.assertIn(f'add_{model}', bazaar_superuser_permissions)
                self.assertIn(f'view_{model}', bazaar_superuser_permissions)
                
            self.assertIn(f'change_{model}', bazaar_superuser_permissions)
            self.assertIn(f'delete_{model}', bazaar_superuser_permissions)