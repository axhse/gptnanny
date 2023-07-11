import logging
from abc import ABC, abstractmethod
from random import random
from time import sleep
from typing import List, Optional

from xata import XataClient

LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(self, title: str, href: str):
        self.title: str = title
        self.href: str = href


class Answer:
    def __init__(self, message: str, sources: List[Source]):
        self.message: str = message
        self.sources: List[Source] = sources


class Consultant(ABC):
    @abstractmethod
    def ask(self, question: str) -> Optional[Answer]:
        pass

    @abstractmethod
    def is_valid_question(self, question: Optional[str]) -> bool:
        pass


class MockConsultant(Consultant):
    def ask(self, question: str) -> Optional[Answer]:
        sleep(1 + random() * 3)
        if question.lower() in ["error", "null", "none"]:
            return None
        source = Source("Google", "https://google.com")
        answer = Answer("[The answer will be here]", [source])
        return answer

    def is_valid_question(self, question: Optional[str]) -> bool:
        return question is not None and 1 <= len(question) <= 500


class XataConsultant(Consultant):
    def __init__(self, api_key: str, db_url: str):
        self.__client: XataClient = XataClient(api_key=api_key, db_url=db_url)

    def ask(self, question) -> Optional[Answer]:
        try:
            payload = {"question": question}
            resp = self.__client.search_and_filter().askTable(
                "knowledge", payload, "nanny", "main"
            )
            if resp.status_code != 200:
                return None
            answer = Answer(resp.json()["answer"], list())
            for source_id in resp.json()["records"][:1]:
                source = self.__client.records().getRecord(
                    "knowledge", source_id, "nanny", "main"
                )
                answer.sources.append(
                    Source(source.json()["title"], source.json()["href"])
                )
            return answer
        except Exception as error:
            LOGGER.error(error)
            return None

    def is_valid_question(self, question: Optional[str]) -> bool:
        # TODO?: check symbols and language
        return question is not None and 1 <= len(question) <= 500
