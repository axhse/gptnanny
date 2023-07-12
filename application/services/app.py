from os import environ

from .appconf import P, get_conf
from .consultant import MockConsultant, XataConsultant
from .question_handler import QuestionHandler
from .secret import S, Secrets
from .translator import LectoTranslator, MockTranslator


class App:
    def __init__(self, question_handler: QuestionHandler):
        self.question_handler: QuestionHandler = question_handler


def build_app() -> App:
    conf_name = environ.get("APP_CONF_NAME", "mock")
    conf = get_conf(conf_name)
    secrets = Secrets()
    if conf[P.IS_MOCK]:
        consultant = MockConsultant()
        translator = MockTranslator()
    else:
        consultant = XataConsultant(secrets[S.XATA_API_KEY])
        translator = LectoTranslator(secrets[S.LECTO_API_KEY])
    return App(QuestionHandler(consultant, translator))


APP = build_app()
