import traceback
from datetime import datetime
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from parser.base.data_typing import Rating
from parser.base.parsers import AbstractSeleniumParser
from parser.constants import YANDEX_TOTAL_RATING_XPATH_LIST, YANDEX_REVIEWS_COUNT_XPATH, YANDEX_REVIEWS_REGARD_XPATH, \
    TWO_GIS_TOTAL_RATING_XPATH_LIST, TWO_GIS_REVIEWS_COUNT_XPATH, TWO_GIS_REVIEWS_REGARD_XPATH
from parser.enums import SourceEnum

import re

from parser.exc import ErrorDataSerializing
from parser.logging_ import logger


class BaseRatingSerializer:
    def regex_cleaning(self, element: WebElement, pattern: str) -> str | None:
        if isinstance(element, WebElement):
            value = element.text
        else:
            return None

        similar_texts = re.findall(pattern, value)
        if similar_texts:
            return similar_texts[0]

    def clean_reviews_regard(self, element: WebElement):
        return self.regex_cleaning(element, r'([\d]*)')

    def clean_total_rating(self, element: WebElement) -> str:
        value = self.regex_cleaning(element, r'([\d][,|\.][\d])')
        if value is None:
            value = self.regex_cleaning(element, r'([\d])')
        return value

    def clean_reviews_count(self, element: WebElement) -> str:
        return self.regex_cleaning(element, r'([\d]*)')

    def serialize(self, data: dict) -> Rating:
        try:
            return Rating(
                source=data.get('source'),
                store=data.get('store'),
                total_rating=self.clean_total_rating(data.get('total_rating')),
                reviews_count=self.clean_reviews_count(data.get('reviews_count')),
                reviews_regard=self.clean_reviews_regard(data.get('reviews_regard')),
                date=data.get('date'),
            )
        except Exception as e:
            logger.debug(traceback.format_exception(e))
            raise ErrorDataSerializing()


class YandexSerializer(BaseRatingSerializer):
    pass


class TwoGisSerializer(BaseRatingSerializer):
    pass


class RatingsSeleniumParser(AbstractSeleniumParser):
    """
    Класс для парсинга рейтингов
    """

    TOTAL_RATING_XPATH_LIST: list
    REVIEWS_REGARD_XPATH: list
    REVIEWS_COUNT_XPATH: list

    def __init__(self):
        super().__init__()
        self.current_store: str | None = None
        self.current_source: str | None = None
        self.now_date = datetime.now().strftime('%d.%m.%Y')
        self.__serializer: BaseRatingSerializer = BaseRatingSerializer()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.web_driver.close()

    def _serialize(self, data: dict) -> Rating:
        data.update(store=self.current_store)
        data.update(source=self.current_source)
        data.update(date=self.now_date)
        return self.__serializer.serialize(data)

    def total_rating_xpath(self):
        for xpath in self.TOTAL_RATING_XPATH_LIST:
            yield xpath

    def reviews_regard_xpath(self):
        for xpath in self.REVIEWS_REGARD_XPATH:
            yield xpath

    def reviews_count_xpath(self):
        for xpath in self.REVIEWS_COUNT_XPATH:
            yield xpath

    def get_attr_data(self, xpath) -> WebElement | None:
        value = False
        while not value:

            try:
                xpath_value = xpath.__next__()
            except StopIteration:
                return None

            try:
                value = self.web_driver.find_element(By.XPATH, xpath_value)
            except NoSuchElementException:
                value = False

        logger.debug(f'get attr by XPATH: {xpath}\nvalue:{value}')

        return value

    def pars(self, url) -> Rating:
        total_rating_xpath = self.total_rating_xpath()
        reviews_regard_xpath = self.reviews_regard_xpath()
        reviews_count_xpath = self.reviews_count_xpath()

        self.web_driver.get(url)

        sleep(3)

        total_rating = self.get_attr_data(total_rating_xpath)
        reviews_regard = self.get_attr_data(reviews_regard_xpath)
        reviews_count = self.get_attr_data(reviews_count_xpath)

        data = {
            'total_rating': total_rating,
            'reviews_regard': reviews_regard,
            'reviews_count': reviews_count,
        }

        return self._serialize(data)

    def logic_source_switcher(self, source: str):
        if source == SourceEnum.YANDEX:
            self.TOTAL_RATING_XPATH_LIST = YANDEX_TOTAL_RATING_XPATH_LIST
            self.REVIEWS_COUNT_XPATH = YANDEX_REVIEWS_COUNT_XPATH
            self.REVIEWS_REGARD_XPATH = YANDEX_REVIEWS_REGARD_XPATH

            self.__serializer = YandexSerializer()

        elif source == SourceEnum.TWO_GIS:
            self.TOTAL_RATING_XPATH_LIST = TWO_GIS_TOTAL_RATING_XPATH_LIST
            self.REVIEWS_COUNT_XPATH = TWO_GIS_REVIEWS_COUNT_XPATH
            self.REVIEWS_REGARD_XPATH = TWO_GIS_REVIEWS_REGARD_XPATH

            self.__serializer = TwoGisSerializer()

    def run(self, url: str, store: str, source: str) -> Rating:
        logger.info(
            (
                f'start parsing:\n'
                f'store: {store}\t\tsource:{source}'
                f'url: {url}'
            )
        )

        self.current_store = store
        self.current_source = source
        self.logic_source_switcher(source)

        # Для 2ГИС сначала пробуем API
        if source == SourceEnum.TWO_GIS:
            from parser.two_gis import TwoGisParser
            tg_parser = TwoGisParser()
            tg_parser.current_store = store
            rating = tg_parser.get_rating_only(url)
            if rating['reviews_count']:  # API вернул данные
                return rating
            # Если API не сработал – идём в Selenium (fallback)

        # Для Яндекса или fallback для 2ГИС – используем старый Selenium-парсер
        return self.pars(url)


if __name__ == '__main__':
    obj = RatingsSeleniumParser()

    # res_y = obj.run(
    #     url='https://yandex.ru/maps/org/alterra/52328578772/reviews/?ll=83.988446%2C53.383425&z=17',
    #     # url='https://yandex.ru/maps/197/barnaul/?ll=83.659632%2C53.353175&mode=poi&poi%5Bpoint%5D=83.659105%2C53.353488&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D130794418046&tab=reviews&z=18',
    #     store='CC',
    #     source=SourceEnum.YANDEX,
    # )
    # res_tg = obj.run(
    #     url='https://2gis.ru/barnaul/branches/563486824415521/firm/563478234508453/83.988881%2C53.384473/tab/reviews',
    #     store='ЦБ',
    #     source=SourceEnum.TWO_GIS,
    # )

    res_tg = obj.run(
        url='https://yandex.ru/maps/org/alterra/1133310706/reviews',
        store='ЦБ',
        source=SourceEnum.YANDEX,
    )

    # print(res_y)
    print(res_tg)
