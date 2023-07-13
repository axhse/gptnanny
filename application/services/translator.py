import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

import requests

from application.services.data_helpers import resp_to_str

LOGGER = logging.getLogger(__name__)


class Lang(Enum):
    EN = "en"
    RU = "ru"


class Translator(ABC):
    @abstractmethod
    def translate(
        self, text: str, lang_to: Lang, lang_from: Optional[Lang] = None
    ) -> Optional[str]:
        pass


class MockTranslator(Translator):
    def translate(
        self, text: str, lang_to: Lang, lang_from: Optional[Lang] = None
    ) -> Optional[str]:
        if lang_from is None:
            return f"[{text}] translated to {lang_to.value}"
        return f"[{text}] translated from {lang_from.value} to {lang_to.value}"


class LectoTranslator(Translator):
    def __init__(self, api_key: str):
        self.__api_key = api_key

    def translate(
        self, text: str, lang_to: Lang, lang_from: Optional[Lang] = None
    ) -> Optional[str]:
        url = "https://api.lecto.ai/v1/translate/text"
        headers = {
            "X-API-Key": self.__api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        body = {
            "to": [lang_to.value],
            "texts": [text],
        }
        if lang_from is not None:
            body.update({"from": lang_from.value})
        resp = requests.post(url=url, headers=headers, json=body)
        if resp.status_code != 200:
            LOGGER.warning(resp_to_str(resp))
            return None
        return resp.json()["translations"][0]["translated"][0]
