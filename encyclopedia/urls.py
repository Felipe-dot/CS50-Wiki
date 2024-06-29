from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("wiki/<str:title>/edit/", views.edit_page, name="edit_page"),
    path("createNewPage/", views.create_new_page, name="create_page"),
    path('random/', views.random_page, name='random_page'),
    path('search/', views.search, name='search')
]
