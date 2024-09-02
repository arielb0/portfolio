from django.test import TestCase
from bazaar.models import Currency, Category, Ad
import datetime
from datetime import timedelta
from django.core.management import call_command

from bazaar.tests.helpers import Generator

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
        
        