from enum import IntEnum, auto
from typing import Any, Dict


class P(IntEnum):
    IS_MOCK = auto()


ALL_CONF: Dict[str, Dict[P, Any]] = {
    "mock": {
        P.IS_MOCK: True,
    },
    "prod": {
        P.IS_MOCK: False,
    },
}


def get_conf(conf_name: str) -> Dict[P, Any]:
    return ALL_CONF[conf_name]
