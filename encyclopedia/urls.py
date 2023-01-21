from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newpage", views.newpage, name="New Page"),
    path("randomentry", views.randompage, name="random"),
    path("edit/<str:entry>", views.edit, name="edit")
]
