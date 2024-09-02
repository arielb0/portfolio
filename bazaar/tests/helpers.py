import shutil
from scull_suite.settings import MEDIA_ROOT, STATICFILES_DIRS
from bazaar.models import Category
from random import choices
import os

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
    
    