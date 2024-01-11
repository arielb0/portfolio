from django.urls import path
from note import views

app_name = "note"

urlpatterns = [
    path("create", views.CreateNote.as_view(), name = "create"),
    path("<int:pk>", views.ReadNote.as_view(), name = "read"),
    path("<int:pk>/update", views.UpdateNote.as_view(), name = "update"),
    path("<int:pk>/delete", views.DeleteNote.as_view(), name = "delete"),
    path("", views.ListNote.as_view(), name="list")
]
