from django.urls import path
from . import views

#The urls and where they lead
urlpatterns = [
    path("aboutUs/", views.about, name='about'),
    path("", views.search, name="home"),
    path("resultPage/", views.results, name="results"),
    path("search/", views.search, name="search"),
    path("query/", views.query, name="query")
]