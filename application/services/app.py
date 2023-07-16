import logging
from os import environ

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db import OperationalError

from .appconf import P, get_conf
from .consultant import Consultant, MockConsultant, XataConsultant
from .question_handler import QuestionHandler
from .translator import LectoTranslator, MockTranslator, Translator

LOGGER = logging.getLogger(__name__)


def create_manager(manager_token: str):
    try:
        user, _ = User.objects.get_or_create(username="manager")
        user.set_password(manager_token)
        content_type = ContentType.objects.get_for_model(User)
        manager_permission, _ = Permission.objects.get_or_create(
            codename="manage", content_type=content_type
        )
        manager_permission.save()
        user.user_permissions.add(manager_permission)
        user.save()
    except OperationalError as error:
        LOGGER.error(error)


class App:
    def __init__(self, consultant: Consultant, translator: Translator):
        self.consultant: Consultant = consultant
        self.question_handler: QuestionHandler = QuestionHandler(consultant, translator)


def build_app() -> App:
    create_manager(environ["MANAGER_TOKEN"])
    conf_name = environ.get("APPCONF", "mock")
    conf = get_conf(conf_name)
    if conf[P.IS_MOCK]:
        consultant = MockConsultant()
        translator = MockTranslator()
    else:
        consultant = XataConsultant(environ["XATA_API_KEY"])
        translator = LectoTranslator(environ["LECTO_API_KEY"])
    return App(consultant, translator)


APP = build_app()
