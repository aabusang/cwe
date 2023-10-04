from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("", views.index, name="home"),    
    path("about/", views.about, name="about"),
    path("login/", views.login, name="login"),
    
    # path("explore/", views.explore, name="datashow-explore"),    
    path("explore/", views.explore, name="explore"),
    
    path("upload/", views.upload, name="upload"),
    path("river/<str:river_name>", views.river, name="river"),

    
    path("not_found/", views.not_found, name="not-found"),
    path("test/", views.test, name="datashow-test")
]
