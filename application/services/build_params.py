from enum import IntEnum, auto
from typing import Any, Dict


class P(IntEnum):
    IS_MOCK = auto()


BUILDS: Dict[str, Dict[P, Any]] = {
    "mock": {
        P.IS_MOCK: True,
    },
    "prod": {
        P.IS_MOCK: False,
    },
}
