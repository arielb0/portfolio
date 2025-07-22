import shutil
from scull_suite.settings import MEDIA_ROOT, STATICFILES_DIRS
from bazaar.models import Currency, Category, Ad, Report, Profile, Review
from django.contrib.auth.models import User
from random import choices
import os
from django.test.client import Client
from django.test import TestCase
from typing import List
from datetime import date

class Generator():
    '''
        This class generate generic objects that I want to use
        for testing purpouses.
    '''

    def create_currency_model(self, name, code) -> Currency:
        '''
            Create and save a currency model
        '''
        currency = Currency(name = name, code = code)
        currency.save()
        return currency

    def create_category_model(self, name, priority) -> Category:
        '''
            Create a Category model object with the following data:

            picture: /img/grocery.webp
        '''

        picture = f'{MEDIA_ROOT}/images/categories/grocery.webp'
        if not os.path.exists(picture):
            shutil.copy(f'{STATICFILES_DIRS[0]}/img/grocery.webp', picture)

        category = Category(name = name, picture = picture, priority = priority)
        category.save()

        return category
    
    def create_ad_model(self, title: str, description: str, price: float
                        , currency: Currency, date: date, category: Category, status: int
                        , rank: int, owner: User) -> Ad:
        '''
            Create a ad model.
        '''

        ad = Ad(title = title, description = description, price = price
                , currency = currency, date = date, category = category,
                status = status, rank = rank, owner = owner)
        ad.save()

        return ad
    
    def create_report_model(self, reason: int, description: str, ad: Ad):
        '''
            Create a Report model
        '''

        report = Report(reason = reason, description = description, ad = ad)
        report.save()

        return report    
    
    def create_user_model(self, username: str, password: str) -> User:
        '''
            Create a user model
        '''

        user_model = User.objects.create_user(username = username, password = password)
        user_model.save()
        return user_model
    
    
    def create_profile_model(self, user, address, phone):
        '''
            Create Profile model
        '''

        profile_model = Profile.objects.create(
            user = user, 
            address = address,
            phone = phone
            )
        profile_model.save()
        
        return profile_model
    
    def create_review_model(self, rating, comment, reviewer, reviewed):
        '''
            Create Review model
        '''

        review_model = Review(
            rating = rating,
            comment = comment,
            reviewer = reviewer,
            reviewed = reviewed
        )
        review_model.save()

        return review_model

    
    def generate_random_string(self, length:int) -> str:
        '''
            Generate random string (numbers characters) with specific length.

            Attributes
            ----------
            length: The number of character present on random string.

            Returns
            -------
            A generated random string with a specific length.
        '''

        return ''.join(choices('0 1 2 3 4 5 6 7 8 9 0'.split(' '), k = length))
    
def get_view_status_code(client: Client, url: str, username: str, password: str) -> int:
    '''
        This function return the status code returned by a view. Useful to test
        authentication and authorization without write repetitive code.

        Parameters
        ----------
        client: Client
            A client used to make request to the view.

        url: str
            A url associated with the Django view.

        username: str
            A username that make the request.

        password: str
            Password used by user.

        Returns
        -------
        int
            The status code of the view.
    '''

    client.login(username = username, password = password)
    response = client.get(url)
    return response.status_code

def test_view_test_func(testcase: TestCase, url: str):
    '''
        This function encapsulates common code used to test test_func method
        present on several views. Useful to avoid repetitive code.
    '''

    testcase.assertEqual(get_view_status_code(testcase.client, url, testcase.GLOBAL_SUPERUSER_USERNAME, testcase.PASSWORD), 200)
    testcase.assertEqual(get_view_status_code(testcase.client, url, testcase.BAZAAR_SUPERUSER_USERNAME, testcase.PASSWORD), 200)
    testcase.assertEqual(get_view_status_code(testcase.client, url, testcase.MODERATOR_USERNAME, testcase.PASSWORD), 403)
    testcase.assertEqual(get_view_status_code(testcase.client, url, testcase.REGULAR_USERNAME, testcase.PASSWORD), 403)
    
    