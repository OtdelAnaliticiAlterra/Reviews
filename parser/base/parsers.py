from abc import ABC

from selenium.webdriver import Chrome
from requests import Response, Session

from parser.base.data_typing import Review


class ParseSessionInterface(ABC):
    """
    Базовый интерфейс парсера отзывов
    """

    def _serialize(self, data: dict | list) -> Review | list[Review]:
        """
        Метод для преобразования полученных из источника данных к единому виду
        """
        raise NotImplementedError

    def pars(self, url: str) -> list[Review]:
        """
        Метод непосредственно для получения данных из источника

        Должен использоваться для получения данных с конкретной страницы сайта
        """
        raise NotImplementedError

    def pars_list(self, urls: list[str]) -> list[Review]:
        """
        Метод для получения данных с группы страниц
        принимает список ссылок
        """
        raise NotImplementedError

    def run(self, url: str | list[str]) -> list[Review]:
        """
        Метод для инициализации парсинга

        Так же может выступать в качестве переключателя метода получения данных по группе источников либо по конкретному
        """
        raise NotImplementedError


class AbstractRequestsParser(ABC):
    """
    Абстрактный класс для реализации парсинга с использованием библиотеки requests

    В классе наследнике реализующем данный класс (AbstractRequestsParser)
    атрибуты BASE_PARAMS и HEADERS должны быть переопределены
    BASE_PARAMS используется для инициализации базовых параметров используемых в запросах
    HEADERS используется для инициализации заголовков HTTP запросов (при инициализации объекта устанавливаются на всю сессию)
    """
    BASE_PARAMS: dict
    HEADERS: dict

    def __init__(self) -> None:
        """
        При инициализации создается объект сессии (класса Session модуля requests)
        """
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


class AbstractSeleniumParser(ABC):
    """
    Абстрактный класс для реализации парсера с использованием библиотеки Selenium
    """

    def __init__(self):
        """
        При инициализации создается объект Chrome драйвера
        """
        self.web_driver: Chrome = self._init_web_driver()

        self.web_driver.maximize_window()

    def _init_web_driver(self) -> Chrome:
        return Chrome()
