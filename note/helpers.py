from django.http import HttpRequest

def set_owner(request: HttpRequest):
    post_attributes = request.POST.copy()
    post_attributes["owner"] = request.user.id
    request.POST = post_attributes
    return request

def is_user_the_owner(self) -> bool:
    return self.get_object().owner.id == self.request.user.id