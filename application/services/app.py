from os import environ

from .appconf import P, get_conf
from .consultant import Consultant, MockConsultant, XataConsultant
from .secret import S, Secrets


class App:
    def __init__(self, consultant: Consultant):
        self.consultant: Consultant = consultant


def build_app() -> App:
    conf_name = environ.get("APP_CONF_NAME", "mock")
    conf = get_conf(conf_name)
    secrets = Secrets()
    if conf[P.IS_CONSULTANT_MOCK]:
        consultant = MockConsultant()
    else:
        consultant = XataConsultant(secrets[S.XATA_DB_URL], secrets[S.XATA_DB_URL])
    return App(consultant)


APP = build_app()
