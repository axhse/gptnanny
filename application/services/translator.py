import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple

import requests

from application.services.data_helpers import resp_to_str

LOGGER = logging.getLogger(__name__)


class Lang(Enum):
    EN = "en"
    RU = "ru"


def str_to_lang(lang_code: Optional[str]) -> Optional[Lang]:
    try:
        return Lang(lang_code)
    except ValueError:
        return None


class Translator(ABC):
    @abstractmethod
    def translate(
        self, text: str, lang_to: Lang, lang_from: Optional[Lang] = None
    ) -> Optional[Tuple[str, Optional[Lang]]]:
        pass


class MockTranslator(Translator):
    def translate(
        self, text: str, lang_to: Lang, lang_from: Optional[Lang] = None
    ) -> Optional[Tuple[str, Optional[Lang]]]:
        return text, lang_to


class LectoTranslator(Translator):
    def __init__(self, api_key: str):
        self.__api_key = api_key

    def translate(
        self, text: str, lang_to: Lang, lang_from: Optional[Lang] = None
    ) -> Optional[Tuple[str, Optional[Lang]]]:
        if lang_to == lang_from:
            return text, lang_from
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
        LOGGER.debug(resp_to_str(resp))
        if resp.status_code != 200:
            return None, None
        translated_text = resp.json()["translations"][0]["translated"][0]
        if lang_from is None:
            lang_from = str_to_lang(resp.json()["from"])
        return translated_text, lang_from


def is_already_translated(resp) -> bool:
    if resp.status_code != 500:
        return False
    message = resp.json().get("error", dict()).get("message", "")
    # Check if the message contains 'service: Translate_{LANG}_{LANG}' substring.
    _, _, lang_info = message.partition("service: Translate_")
    if lang_info == "":
        return False
    lang_from, _, lang_to_info = lang_info.partition("_")
    if lang_to_info == "":
        return False
    lang_to = lang_to_info.partition(",")[0]
    return lang_from == lang_to


class SystranTranslator(Translator):
    def __init__(self, api_key: str):
        self.__api_key = api_key

    def translate(
        self, text: str, lang_to: Lang, lang_from: Optional[Lang] = None
    ) -> Optional[Tuple[str, Optional[Lang]]]:
        if lang_to == lang_from:
            return text, lang_to
        url = "https://api-translate.systran.net/translation/text/translate"
        params = {
            "key": self.__api_key,
            "input": text,
            "target": lang_to.value,
            "withInfo": True,
        }
        if lang_from is not None:
            params.update({"source": lang_from.value})
        resp = requests.post(url=url, params=params)
        LOGGER.debug(resp_to_str(resp))
        if resp.status_code != 200:
            # When the text is already translated response also has a error.
            if is_already_translated(resp):
                return text, lang_to
            return None, None
        translated_text = resp.json()["outputs"][0]["output"]
        if lang_from is None:
            lang_from = str_to_lang(
                resp.json()["outputs"][0]["info"]["lid"]["language"]
            )
        return translated_text, lang_from
