from os import environ

from .build_params import BUILDS, P
from .consultant import Consultant, MockConsultant, XataConsultant
from .question_handler import QuestionHandler
from .translator import LectoTranslator, MockTranslator, Translator


class App:
    def __init__(self, consultant: Consultant, translator: Translator):
        self.consultant: Consultant = consultant
        self.question_handler: QuestionHandler = QuestionHandler(consultant, translator)


def build_app() -> App:
    build_params = BUILDS[environ.get("BUILD_NAME", "mock")]
    if build_params[P.IS_MOCK]:
        consultant = MockConsultant()
        translator = MockTranslator()
    else:
        consultant = XataConsultant(environ["XATA_API_KEY"])
        translator = LectoTranslator(environ["LECTO_API_KEY"])
    return App(consultant, translator)


APP = build_app()
