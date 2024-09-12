from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from os.path import splitext
from sys import getsizeof
from django.http import HttpRequest
from .models import Category
from django.db.models import QuerySet
from .forms import SimpleSearchForm
from typing import Any

def create_thumbnail(image_field: InMemoryUploadedFile, size: tuple[int]):
    '''
        Create a JPEG thumbnail from image field.

        Parameters
        ----------
        image_field : InMemoryUploadedFile 
            A InMemoryUploadedFile object that contains a image file.
        size: (int, int) 
            A tuple that specify thumbnail image size (width, height).

        Returns 
        -------

        InMemoryUploadedFile
            A InMemoryUploadedFile object with a thumbnail
    '''

    normalized_image = BytesIO()
    image = Image.open(image_field.file)    
    image_name = splitext( image_field.name)[0]

    image = image.convert('RGB')
    image.thumbnail(size)
    
    image.save(normalized_image, 'JPEG')
    normalized_image.seek(0)
    
    return InMemoryUploadedFile(normalized_image, image_field.field_name, 
                                f'{image_name}.jpg', 
                                'image/jpeg', 
                                getsizeof(normalized_image), None)

def normalize_ad_pictures(request: HttpRequest, size: tuple[int]):
    '''
        Normalize ad pictures (reduce picture size and convert to JPEG format).
        This function modify their input (request). Is not a pure function.
        
        Parameters:
        -----------
        request: HttpRequest
            A HttpRequest with ad pictures fields to be normalized

        Returns:
        HttpRequest
            A HttpRequest with ad pictures fields normalized.
    '''

    normalized_request = HttpRequest()
    
    normalized_request.path = request.path
    normalized_request.path_info = request.path_info
    normalized_request.method = request.method
    normalized_request.encoding = request.encoding
    normalized_request.content_type = request.content_type
    normalized_request.content_params = request.content_params
    normalized_request.GET = request.GET.copy()
    normalized_request.POST = request.POST.copy()
    normalized_request.COOKIES = request.COOKIES.copy()
    normalized_request.META = request.META.copy()
    normalized_request.headers = request.headers
    normalized_request.resolver_match = request.resolver_match

    for number in range(0, 10):
            field_name = f'picture_{number}'
            if field_name in request.FILES.keys():
                normalized_request.FILES[field_name] = create_thumbnail(request.FILES[field_name], size)
    
    return normalized_request

def get_simple_search_form(context: dict[str, Any], data: dict = {}):
     '''
        This function return SimpleSearchForm instance on the passed context.

        Parameters
        -----------
        context : dict[str] dict A Django view context
        data : dict The initial value for SimpleSearchForm. Default value is an empty dictionary.

        Returns
        --------
        Context with simple_search_form key and SimpleSearchForm form value
     '''
     
     context_copy = context.copy()
     context_copy['simple_search_form'] = SimpleSearchForm(data = data)
     return context_copy
