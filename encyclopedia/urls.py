from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title_search, name="title_search"),
    path("search",views.search, name="search"),
    path("newpage",views.new_page, name="newpage"),
    path("wiki/<str:title>/edit",views.edit_display, name="edit_display"),
    path("wiki/<str:title>/submit",views.edit_submit, name="edit_submit"),
    path("wiki/",views.random_page, name="random_page")
]

