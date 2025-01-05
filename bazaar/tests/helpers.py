import shutil
from scull_suite.settings import MEDIA_ROOT, STATICFILES_DIRS
from bazaar.models import Category
from django.contrib.auth.models import User
from random import choices
import os
from django.test.client import Client
from django.test import TestCase

class Generator():
    '''
        This class generate generic objects that I want to use
        for testing purpouses.
    '''

    def create_category_model(self) -> Category:
        '''
            Create a Category model object with the following data:

            name: Groceries
            picture: /img/grocery.webp
            priority: 1
        '''

        picture = f'{MEDIA_ROOT}/images/groups/grocery.webp'
        if not os.path.exists(picture):
            shutil.copy(f'{STATICFILES_DIRS[0]}/img/grocery.webp', picture)

        category = Category(name = 'Groceries', picture = picture, priority = 1)
        category.save()

        return category
    
    def create_user_model(self):
        '''
            Create a user model with the following data:
            username: Peter
            password: insecurePassw0rD!@
        '''

        user_model = User.objects.create_user(username = 'Peter', password = 'insecurePassw0rD!@')
        user_model.save()
        return user_model
    
    def create_ad_model(self):
        '''
            Create a ad model with the following data:

            title: I sell cucumbers
            description: I have some fresh cucumbers.
            price: 10
            currency: A model created with create_currency_model() method
            address: Kennedy Street, 45
            name:
        '''

    
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
    
    