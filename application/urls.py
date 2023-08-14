from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.homepage),
    path("ask", views.ask),
    path("login", views.check_password),
    path("manage", views.login_as_manager),
    path("articles", views.get_articles),
    path("article/edit/<article_id>", views.edit_article),
    path("article/create", views.create_article),
    path("article/update", views.update_article),
    path("article/delete", views.delete_article),
    re_path(r"^", views.redirect_to_homepage),
]
