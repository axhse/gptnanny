from enum import IntEnum, auto
from os import environ
from typing import Dict, Optional


class S(IntEnum):
    XATA_API_KEY = auto()
    LECTO_API_KEY = auto()


class Secrets:
    def __init__(self):
        self.__values: Dict[S, str] = dict()
        for secret in S:
            if secret.name in environ:
                self.__values[secret] = environ[secret.name]

    def get_or_none(self, secret: S) -> Optional[str]:
        return self.__values.get(secret)

    def __getitem__(self, secret: S) -> str:
        return self.__values[secret]
