from enum import IntEnum, auto
from os import environ
from typing import Dict, Optional


class S(IntEnum):
    TRANSLATOR_API_KEY = auto()
    XATA_API_KEY = auto()
    XATA_DB_URL = auto()


class Secrets:
    def __init__(self):
        names = set(environ.keys()).intersection({s.name for s in S})
        self.__values: Dict[S, str] = {name: environ[name] for name in names}

    def get_or_none(self, secret: S) -> Optional[str]:
        return self.__values.get(secret)

    def __getitem__(self, secret: S) -> str:
        return self.__values[secret]
