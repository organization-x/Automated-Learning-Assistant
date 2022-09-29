from django.urls import path
from . import views

urlpatterns = [
    path("aboutUs/", views.about, name='about'),
    path("", views.home, name="home"),
    path("resultPage/", views.results, name="results")
]
