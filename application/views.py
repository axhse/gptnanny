import json
import logging

from django.http import HttpResponse
from django.shortcuts import render

from .services.app import APP

# Create your views here.


LOGGER = logging.getLogger(__name__)


def homepage(request):
    return render(request, "consultant.html")


def ask(request):
    question = str(request.POST.get("question"))
    LOGGER.info(f"Question[{question}]")
    answer = APP.consultant.ask(question)
    if answer is None:
        LOGGER.info(f"Answer is null")
        return HttpResponse(status=500)
    else:
        response_data = {
            "message": answer.message,
            "sources": [
                {"title": source.title, "href": source.href}
                for source in answer.sources
            ],
        }
        LOGGER.info(f"Message[{answer.message}]")
        return HttpResponse(json.dumps(response_data), content_type="application/json")
