from django.urls import path

from . import views
from . import forms


urlpatterns = [
    path("", views.index, name="index"),
    path("", views.index, name="home"),    
    path("about/", views.about, name="about"),
    path("login/", views.login, name="login"),
    
    #Explore page

    path("explore/", views.explore, name="explore"),

    #Download page
    path("download/", views.download_view, name="download_view"),
    path('download/', views.download_csv, name='download_csv'),
    # path('download/csv/', views.download_csv, name='download_csv'),

    #Upload page
    path("upload/", views.upload, name="upload"),

    path("docs/", views.docs, name="docs"),

    path("not_found/", views.not_found, name="not-found"),
]
