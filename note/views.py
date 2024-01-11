from typing import Any, Optional
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from note.models import Note
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from note.forms import NoteForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q


# Create your views here.

class CreateNote(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("note:list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        request = set_owner(request)
        return super().post(request, *args, **kwargs)


class ReadNote(UserPassesTestMixin, DetailView):
    model = Note
    
    def test_func(self) -> bool | None:
        return is_user_the_owner(self)


class UpdateNote(UserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("note:list")
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        request = set_owner(request)
        return super().post(request, *args, **kwargs)
    
    def test_func(self) -> bool | None:
        return is_user_the_owner(self)


class DeleteNote(UserPassesTestMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("note:list")

    def test_func(self) -> bool | None:
        return is_user_the_owner(self)

class ListNote(LoginRequiredMixin, ListView):
    model = Note

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.GET.__contains__("search"):
            search_pattern = self.request.GET["search"]
            return Note.objects.filter(owner_id=self.request.user.id).filter(Q(title__contains=search_pattern) | Q(body__contains=search_pattern) | Q(tags__contains=search_pattern))
                  
        return Note.objects.filter(owner_id=self.request.user.id)

def set_owner(request: HttpRequest):
    post_attributes = request.POST.copy()
    post_attributes["owner"] = request.user.id
    request.POST = post_attributes
    return request

def is_user_the_owner(self) -> bool:
    return self.get_object().owner.id == self.request.user.id