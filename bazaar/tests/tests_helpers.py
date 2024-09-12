from django.test import TestCase
from ..helpers import create_thumbnail, normalize_ad_pictures, get_simple_search_form
from django.core.files.uploadedfile import InMemoryUploadedFile
from scull_suite.settings import STATICFILES_DIRS
from os.path import join
from PIL import Image
from sys import getsizeof
from django.test import RequestFactory
from django.urls import reverse
from ..models import Category, Currency
from os.path import splitext
from ..forms import SimpleSearchForm


from bazaar.tests.helpers import Generator

class NormalizePictureTestSuite(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        cls.FILENAME = 'smartphone.webp'
        cls.CONTENT_TYPE = 'image/webp'
        cls.THUMBNAIL_SIZE = (120, 120)

        cls.generator = Generator()        

        return super().setUpTestData()
    
    def test_create_thumbnail(self):
        '''
            Test if create_thumbnail function returns a 
            InMemoryUploadedFile object with correct attributes:

            file: a JPEG file
            field_name: a passed field name (picture_0)
            name: filename with jpg extension
            content_type: image/jpeg
            size: picture file size

            Also, I need to verify file properties, like:

            format: jpeg
            size: the size should be similar to thumbnail size.
        '''

        '''
            Pseudocode:

            1 Create a InMemoryUploaded object, that contain
            a picture on another format.

            2 Execute create_thumbnail function

            3 Check if create_thumbnail function returns a 
            InMemoryUploaded object with JPEG thumbnail.
        '''
        
        filename = 'smartphone.webp'
        field_name = 'picture_0'
        content_type = 'image/webp'
        thumbnail_size = (120, 120)
        picture = open(join(STATICFILES_DIRS[0], 'img', filename), 'rb')
                
        picture_field = InMemoryUploadedFile(
            file=picture, 
            field_name=field_name, 
            name=filename, 
            content_type='image/webp', 
            size=getsizeof(picture), 
            charset=None
        )

        thumbnail_field = create_thumbnail(picture_field, thumbnail_size)
        thumbnail_file = Image.open(thumbnail_field.file)

        self.assertEqual(thumbnail_field.field_name, field_name)
        self.assertEqual(thumbnail_field.name, 'smartphone.jpg')
        self.assertEqual(thumbnail_field.content_type, 'image/jpeg')
        self.assertEqual(thumbnail_field.size, getsizeof(thumbnail_field.file))

        self.assertEqual(thumbnail_file.format, 'JPEG')
        self.assertEqual(thumbnail_file.size[0], thumbnail_size[0]) # Why works with the 0? 

    def test_normalize_ad_pictures(self):
        '''
            Test if normalize_ad_pictures function convert to JPEG format and reduce
            size of several files
        '''

        '''
            1 Create a HttpRequest object with an ad containing several pictures fields.
            2 Normalize ad pictures using normalize_ad_pictures function
            3 Test if ad pictures are normalized.
        '''
        currency = Currency(name='United States Dollar', code='USD')
        currency.save()
        '''
        group_picture = f'{MEDIA_ROOT}/images/groups/grocery_category.webp'
        shutil.copy(f'{STATICFILES_DIRS[0]}/img/grocery_category.webp', group_picture)

        category_group = CategoryGroup(name = 'Test Group', picture = group_picture, priority = 0)
        category_group.save()
        '''
        # category_group = self.generator.create_category_group_model()

        category = Category(name='Test Category', priority = 1)
        category.save()
        
        factory = RequestFactory()
        thumbnail_size = (120, 120)

        request_data = {
            'title': 'An ad to normalize pictures',
            'description': 'This ad is to test if normalize_pictures\
                    function can do its job well.',
            'price': 1000,
            'currency': currency.pk,
            'address': 'Oak Street, Palo Alto, California',
            'name': 'George Huntington',
            'phone': 1234567890,
            'mail': 'georgeh2002@protonmail.com',
            'category': category.pk,            
        }
        
        picture = open(join(STATICFILES_DIRS[0], 'img', self.FILENAME), 'rb')        
        
        request = factory.post(
            reverse('bazaar:ad_create'),
            request_data,
        )

        for number in range(0, 10):
            field_name = f'picture_{number}'
            request.FILES[field_name] = InMemoryUploadedFile(
                file = picture,
                field_name = field_name,
                name = self.FILENAME,
                content_type = self.CONTENT_TYPE,
                size = getsizeof(picture),
                charset = None
            )
                
        normalized_request = normalize_ad_pictures(request, thumbnail_size)

        for number in range(0, 10):

            field_name = f'picture_{number}'
            normalized_field = normalized_request.FILES[field_name]
            normalized_picture = Image.open(normalized_field)

            self.assertEqual(normalized_picture.format, 'JPEG')
            self.assertEqual(normalized_picture.size[0], thumbnail_size[0])

            self.assertEqual(normalized_field.field_name, field_name)
            self.assertEqual(normalized_field.name, f'{splitext(self.FILENAME)[0]}.jpg')
            self.assertEqual(getsizeof(normalized_field.file), normalized_field.size)

    def test_get_simple_search_form(self):
        '''
            Test if get_simple_search_form implements the right logic
            (return a view context with a SimpleSearchForm instance, populated with
            passed data)
        '''

        context = get_simple_search_form(context = {}, data={'query':'groceries'})

        self.assertIn('simple_search_form', context)
        self.assertIsInstance(context['simple_search_form'], SimpleSearchForm)
        self.assertEqual(context['simple_search_form']['query'].data, 'groceries')
