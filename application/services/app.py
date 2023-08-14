from os import environ

from .build_params import BUILD_PARAMS, P
from .chatbot import ChatBot
from .consultant import Consultant, MockConsultant, XataConsultant
from .translator import MockTranslator, SystranTranslator, Translator


class App:
    def __init__(self, consultant: Consultant, translator: Translator):
        self.consultant: Consultant = consultant
        self.chat_bot: ChatBot = ChatBot(consultant, translator)


def build_app() -> App:
    build_params = BUILD_PARAMS[environ.get("BUILD_NAME", "mock")]
    if build_params[P.IS_MOCK]:
        consultant = MockConsultant()
        translator = MockTranslator()
    else:
        consultant = XataConsultant(environ["XATA_API_KEY"])
        translator = SystranTranslator(environ["SYSTRAN_API_KEY"])
    return App(consultant, translator)


APP = build_app()
