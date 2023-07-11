import json

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .services.app import APP

# Create your views here.


def homepage(request):
    return render(request, "consultant.html")


def redirect_to_homepage(request):
    return redirect(homepage)


def ask(request):
    question = str(request.POST.get("question"))
    if not APP.consultant.is_valid_question(question):
        return HttpResponse(status=400)
    answer = APP.consultant.ask(question)
    if answer is None:
        return HttpResponse(status=500)
    else:
        response_data = {
            "message": answer.message,
            "sources": [
                {"title": source.title, "href": source.href}
                for source in answer.sources
            ],
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
