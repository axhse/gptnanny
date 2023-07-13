from typing import Optional

from application.services.consultant import Answer, Consultant
from application.services.tracing import Event, Tracing
from application.services.translator import Lang, Translator


class QuestionHandler:
    def __init__(self, consultant: Consultant, translator: Translator, tracing: Tracing):
        self.__consultant: Consultant = consultant
        self.__translator: Translator = translator
        self.__tracing: Tracing = tracing

    def ask(self, question: str) -> Optional[Answer]:
        trace = self.__tracing.create()
        trace.add(Event("question", question))
        translated_question = self.__translator.translate(question, Lang.EN)
        if translated_question is None:
            return None
        trace.add(Event("translated question", translated_question))
        answer = self.__consultant.ask(translated_question)
        if answer is None:
            return None
        trace.add(Event("answer", answer.json()))
        answer.message = self.__translator.translate(answer.message, Lang.RU, Lang.EN)
        if answer.message is None:
            return None
        trace.add(Event("translated message", answer.message))
        return answer
