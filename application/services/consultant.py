import logging
from abc import ABC, abstractmethod
from random import random
from time import sleep
from typing import List, Optional

from xata import XataClient

from application.services.data_helpers import resp_to_str

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


class MockConsultant(Consultant):
    def ask(self, question: str) -> Optional[Answer]:
        sleep(1 + random() * 3)
        if question.lower() in ["error", "null", "none"]:
            return None
        source = Source("Google", "https://google.com")
        answer = Answer("The answer will be here.", [source])
        return answer


class XataConsultant(Consultant):
    WORKSPACE_ID = "77mmm6"
    REGION = "eu-central-1"
    DB_NAME = "gptnanny"
    TABLE_NAME = "knowledge"
    BRANCH_NAME = "main"

    def __init__(self, api_key: str):
        self.__client: XataClient = XataClient(
            api_key=api_key,
            workspace_id=self.WORKSPACE_ID,
            region=self.REGION,
            db_name=self.DB_NAME,
            branch_name=self.BRANCH_NAME,
        )

    def ask(self, question) -> Optional[Answer]:
        try:
            payload = {"question": question}
            answer_resp = self.__client.search_and_filter().askTable(
                self.TABLE_NAME, payload
            )
            LOGGER.debug(resp_to_str(answer_resp))
            if answer_resp.status_code != 200:
                return None
            answer = Answer(answer_resp.json()["answer"], list())
            source_ids = answer_resp.json()["records"][:1]
            for source_id in source_ids:
                source_resp = self.__client.records().getRecord(
                    self.TABLE_NAME, source_id
                )
                LOGGER.debug(resp_to_str(source_resp))
                if source_resp.status_code != 200:
                    return None
                answer.sources.append(
                    Source(source_resp.json()["title"], source_resp.json()["href"])
                )
            return answer
        except Exception as error:
            LOGGER.error(error)
            return None
