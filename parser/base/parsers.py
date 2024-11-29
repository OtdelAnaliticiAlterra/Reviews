from abc import ABC
from webbrowser import Chrome

from requests import Response, Session

from parser.base.data_typing import Review


class ParseSessionInterface(ABC):

    def _serialize(self, data: dict | list) -> Review | list[Review]:
        raise NotImplementedError

    def pars(self, url: str) -> list[Review]:
        raise NotImplementedError

    def pars_list(self, urls: list[str]) -> list[Review]:
        raise NotImplementedError

    def run(self, url: str | list[str]) -> list[Review]:
        raise NotImplementedError


class AbstractRequestsParser(ABC):
    BASE_PARAMS: dict
    HEADERS: dict

    def __init__(self) -> None:
        self._params: dict = self.BASE_PARAMS
        self._headers: dict = self.HEADERS
        self._session: Session = self._get_session()

    @property
    def params(self) -> dict:
        return self._params.copy()

    @params.setter
    def params(self, data: dict) -> None:
        self._params.update(data)

    @property
    def headers(self) -> dict:
        return self._headers.copy()

    @headers.setter
    def headers(self, data: dict) -> None:
        self._headers.update(data)
        self._session.headers.update(self._headers)

    def _get_session(self) -> Session:
        session = Session()
        session.headers.update(self._headers)
        return session


class AbstractParserInterface(ABC):
    def __init__(self):
        self.web_driver = self._init_web_driver()

    def _init_web_driver(self) -> Chrome:
        return Chrome()
