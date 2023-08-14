import json
from json import JSONDecodeError

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .services import validators
from .services.app import APP
from .services.consultant import Article
from .services.validators import is_valid_password, is_valid_username


def homepage(request):
    return render(request, "consultant.html")


def redirect_to_homepage(request):
    return redirect(homepage, permanent=True)


def ask(request):
    try:
        question = json.loads(request.body).get("question")
    except JSONDecodeError:
        return HttpResponse(status=500)
    if not validators.is_valid_question(question):
        return HttpResponse(status=400)
    answer = APP.chat_bot.ask(question)
    if answer is None:
        return HttpResponse(status=500)
    return HttpResponse(json.dumps(answer.json()), content_type="application/json")


def login_as_manager(request):
    if request.user.has_perm("auth.manage"):
        return redirect(get_articles, permanent=True)
    return render(request, "login_as_manager.html")


def check_password(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if not is_valid_username(username):
        return HttpResponse(status=404)
    if not is_valid_password(password):
        return HttpResponse(status=403)
    user = authenticate(request, username=username, password=password)
    if user is None:
        if User.objects.get(username=username) is None:
            return HttpResponse(status=404)
        return HttpResponse(status=403)
    login(request, user)
    return HttpResponse(status=200)


@permission_required("auth.manage", login_url="/manage")
def get_articles(request):
    articles = APP.consultant.get_articles_short()
    if articles is None:
        return HttpResponse(status=500)
    data = {"articles": articles}
    return render(request, "articles.html", data)


@permission_required("auth.manage", login_url="/manage")
def edit_article(request, article_id):
    article = APP.consultant.get_article(article_id)
    if article is None:
        return HttpResponse(status=404)
    data = {"article": article}
    return render(request, "edit_article.html", data)


@permission_required("auth.manage", login_url="/manage")
def create_article(request):
    article = Article(article_id="")
    data = {"article": article}
    return render(request, "edit_article.html", data)


@permission_required("auth.manage", login_url="/manage")
def update_article(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return HttpResponse(status=500)
    article_id = data.get("id")
    title = data.get("title")
    href = data.get("href")
    content = data.get("content")
    if not (
        validators.is_valid_article_title(title)
        and validators.is_valid_article_href(href)
        and validators.is_valid_article_content(content)
    ):
        return HttpResponse(status=500)
    article = Article(article_id, title, href, content)
    if article_id == "":
        created_id = APP.consultant.create_article(article)
        if created_id is None:
            return HttpResponse(status=500)
        data = {"id": created_id}
        return HttpResponse(json.dumps(data), content_type="application/json")
    if not validators.is_valid_article_id(article_id):
        return HttpResponse(status=500)
    if APP.consultant.update_article(article):
        return HttpResponse(status=200)
    return HttpResponse(status=500)


@permission_required("auth.manage", login_url="/manage")
def delete_article(request):
    article_id = request.POST.get("id")
    if not validators.is_valid_article_id(article_id):
        return HttpResponse(status=500)
    if APP.consultant.delete_article(article_id):
        return HttpResponse(status=200)
    return HttpResponse(status=500)
