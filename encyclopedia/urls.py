from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("wiki/<str:title>/edit/", views.editPage, name="editPage"),
    path("createNewPage/", views.createNewPage, name="createPage"),
    path('random/', views.random_page, name='random_page'),
    path('search/', views.search, name='search')
]
