from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.homepage),
    path("ask", views.ask),
    re_path(r"^", views.redirect_to_homepage),
]
