from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from os.path import splitext
from sys import getsizeof
from django.http import HttpRequest
from .forms import SimpleSearchForm
from accounts.forms import UserAdminForm, UserForm
from django.contrib.auth.forms import PasswordChangeForm
from typing import Any
from bazaar.models import Profile, Review
from django.db.models import Sum

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

def copy_request(request: HttpRequest):
    '''
        This function copy a Django HTTP Request. This is useful to modify the request
        without change the original (functional programming principle)
    '''

    request_copy = HttpRequest()

    request_copy.path = request.path
    request_copy.path_info = request.path_info
    request_copy.method = request.method
    request_copy.encoding = request.encoding
    request_copy.content_type = request.content_type
    request_copy.content_params = request.content_params
    request_copy.GET = request.GET.copy()
    request_copy.POST = request.POST.copy()
    request_copy.COOKIES = request.COOKIES.copy()
    request_copy.META = request.META.copy()
    request_copy.headers = request.headers
    request_copy.resolver_match = request.resolver_match
    
    if hasattr(request, 'user'):
        request_copy.user = request.user
    # TODO: Put more fields.. You will need it.

    return request_copy

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
    normalized_request = copy_request(request)

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
'''
def user_is_superuser(request: HttpRequest) -> bool:
     
        This function return True if user present on request is superuser.
        Useful to avoid repetitive code on views and tests modules.

        Returns
        --------
        Return True if user is superuser, False otherwise.
     
     return request.user.is_superuser
     '''

def get_user_form(request: HttpRequest):
    '''
        This method returns the proper UserForm class
        that CreateProfile or UpdateProfile will use.
        If user that make request is superuser, return UserAdminForm, else
        return UserForm
    '''

    if request.user.is_superuser:
        return UserAdminForm
    
    return UserForm

def get_profile_view_context(request: HttpRequest, context: dict):
     '''
        This function return the passed context with
        user_form and password_form. Useful to avoid repetitive
        code on CreateProfile and UpdateProfile views
     '''     

     if request.user.is_superuser:
        user_form = UserAdminForm()
     else:
        user_form = UserForm()

     context['user_form'] = user_form
     context['password_form'] = PasswordChangeForm

     return context

def set_profile_user(request: HttpRequest):
     '''
        This function modify user on CreateProfile and UpdateProfile views,
        to ensure that the user that make the request is modifing your own
        profile and not another. This function encapsulates repetive code
        present on this views, inside post method.
     '''

     if request.POST['user'] != request.user.id:
        modified_request = copy_request(request)
        modified_request.POST['user'] = request.user.id
        return modified_request

     return request

def get_profile_stats(profile: Profile, context: dict) -> dict:
    '''
        Get profile statistics (number of reviews and average rating)
    '''
    
    reviews = Review.objects.filter(reviewed = profile)
    context['number_of_reviews'] = reviews.count()
    context['average_rating'] = reviews.aggregate(value = Sum('rating') / context['number_of_reviews'])['value']

    return context
        