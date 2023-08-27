from typing import Optional

from application.services.consultant import Answer, Consultant
from application.services.translator import Lang, Translator


class ChatBot:
    def __init__(self, consultant: Consultant, translator: Translator):
        self.__consultant: Consultant = consultant
        self.__translator: Translator = translator

    def ask(self, question: str) -> Optional[Answer]:
        translated_question, lang = self.__translator.translate(question, Lang.EN)
        if translated_question is None:
            return None
        answer = self.__consultant.ask(translated_question)
        if answer is None:
            return None
        if lang is not None:
            translated_message, _ = self.__translator.translate(
                answer.message, lang, Lang.EN
            )
            if translated_message is None:
                return None
            answer.message = translated_message
        if answer.message is None:
            return None
        return answer
