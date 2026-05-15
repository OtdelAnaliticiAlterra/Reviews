from enum import Enum

from requests import Response

from parser.base.parsers import ParseSessionInterface, AbstractRequestsParser, AbstractSeleniumParser
from parser.base.serializers import SerializerInterface
from parser.base.data_typing import Review, User, OfficialAnswer, Rating



class SerializeModeEnum(Enum):
    """
    # НА ТЕКУЩИЙ МОМЕНТ РЕАЛИЗАЦИЯ ДАННОГО ФУНКЦИОНАЛА ПРЕОСТАНОВЛЕНА

    Данный класс используется в качестве значений состояния TwoGisSerializer
    """
    SOFT: str = 'SOFT'  # При установке данного значения возникающие исключения будут игнорироваться
    HARD: str = 'HARD'  # При установке данного значения возникающие исключения НЕ будут игнорироваться, а так же
    # будут подниматься исключения при передаче некорректных данных для преобразования


class TwoGisSerializer(SerializerInterface):
    """
    Класс для преобразования данных полученных с сайта 2Gis

    Реализует интерфейс SerializerInterface
    """

    def __init__(self, mode: SerializeModeEnum):
        self.__mode = mode

    @staticmethod
    def __user_serializer(data: dict) -> User | None:
        """
        Статический метод для преобразования, полученных данных о пользователе, в типизированный словарь User
        """
        if data is None: return None

        user: User = {
            field: data.get(field)
            for field in User.__annotations__.keys()
        }
        return User(**user)

    @staticmethod
    def __official_answer_serializer(data: dict) -> OfficialAnswer | None:
        """
        Статический метод для преобразования, полученных данных об официальном ответе компании, в
        типизированный словарь OfficialAnswer
        """
        if data is None: return None

        official_answer: OfficialAnswer = {
            field: data.get(field)
            for field in OfficialAnswer.__annotations__.keys()
        }
        return OfficialAnswer(**official_answer)

    def _serialize_single(self, data: dict) -> Review:
        """
        Метод для преобразования данных конкретного отзыва в словарь Review
        """
        if not isinstance(data, dict):
            raise ValueError(f'Type {type(data)} is not serializable')
        review: Review = dict()
        for field in Review.__annotations__.keys():
            if field == 'user':
                review.update({field: self.__user_serializer(data.get(field))})
            elif field == 'official_answer':
                review.update({field: self.__official_answer_serializer(data.get(field))})
            else:
                review.update({field: data.get(field)})
        return Review(**review)

    def _serialize_from_list(self, data: list) -> list[Review]:
        """
        Метод для преобразования списка данных об отзывах
        """
        reviews: list[Review] = list()
        for review in data:
            reviews.append(self._serialize_single(review))
        return reviews

    def serialize(self, data: dict | list[dict]) -> Review | list[Review]:
        """
        Метод для запуска преобразования данных.
        Может принимать как словарь с конкретным отзывом так и список словарей содержащий данный отзывов
        """
        if isinstance(data, list):
            return self._serialize_from_list(data)
        elif isinstance(data, dict):
            return self._serialize_single(data)
        else:
            raise ValueError(f'Type {type(data)} is not serializable')


class TwoGisParser(AbstractRequestsParser, ParseSessionInterface):
    """
    Класс реализует интерфейс ParseSessionInterface и абстрактный класс AbstractRequestsParser

    Для получения данных с сайта 2Gis

    Получение данных осуществляется из скрытого API 2Gis для чего достаточно использование модуля requests
    """
    HEADERS: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    BASE_PARAMS: dict = {
        'limit': '50',
        'locale': 'ru_RU',
        'sort_by': 'date_created',
        'fields': 'meta.providers,meta.branch_rating,meta.branch_reviews_count,meta.total_count,reviews.hiding_reason,reviews.is_verified',

        'key': 'b0209295-ae15-48b2-acb2-58309b333c37',
    }

    def __init__(self):
        super().__init__()
        self._serializer = TwoGisSerializer(mode=SerializeModeEnum.SOFT)
        self.current_store: str | None = None

        self._org_id: str | None = None

        self.current_rating_data: dict = dict()
        """
        current_rating_data structure
            'total_rating': 'str',
            'reviews_count': 'str',
            'store': 'str',
            'reviews_regard': 'str',
        """

    @property
    def org_id(self):
        return self._org_id

    @org_id.setter
    def org_id(self, value: str):
        cleaned_value = value.split('/')[-2]
        self._org_id = cleaned_value

    def _serialize(self, data: dict | list[dict]) -> Review | list[Review]:

        if isinstance(data, list):
            reshape_list = list()
            for rev in data:
                rev.update(self.current_rating_data)
                reshape_list.append(rev)
            data = reshape_list
        elif isinstance(data, dict):
            data.update(self.current_rating_data)

        return self._serializer.serialize(data)

    def pars(self, url: str) -> list[Review]:
        """
        При обращении к API 2Gis возвращаются данные в JSON в формате.
        Содержит атрибут next_link который перенаправляет на следующий срез данных с отзывами
        """

        self.org_id = url

        reviews: list = list()
        next_link = url

        while next_link is not None:
            response: Response = self._session.get(next_link, params=self._params)
            reviews_json: dict = response.json().get('reviews')
            reviews.extend(reviews_json)
            next_link = response.json().get('next_link')

            self.get_rating(response.json().get('meta'))

        return self._serialize(reviews)

    def pars_list(self, urls: list[str]) -> list[Review]:
        reviews: list = list()
        for url in urls:
            reviews.extend(self.pars(url))
        return reviews

    def run(self, url: str | list[str], store: str = None) -> list[Review]:

        self.current_store = store

        if isinstance(url, str):
            return self.pars(url)
        elif isinstance(url, list):
            return self.pars_list(url)

    def get_rating(self, rating_data: dict) -> None:
        if rating_data is None:
            return

        self.current_rating_data = {
            'total_rating': rating_data.get('branch_rating'),
            'reviews_count': rating_data.get('branch_reviews_count'),
            'store': self.current_store,
            'reviews_regard': rating_data.get('branch_reviews_count'),
        }

    def get_rating_only(self, branch_url: str):
        """Получает рейтинг и количество отзывов через API 2ГИС."""
        from datetime import datetime
        import re
        from parser.constants import TWO_GIS_API_KEY
        from parser.enums import SourceEnum
        from parser.base.data_typing import Rating

        match = re.search(r'/firm/(\d+)', branch_url)
        if not match:
            return Rating(
                source=SourceEnum.TWO_GIS,
                store=self.current_store,
                total_rating='',
                reviews_count='',
                reviews_regard='',
                date=datetime.now().strftime('%d.%m.%Y')
            )
        branch_id = match.group(1)
        api_url = f"https://public-api.reviews.2gis.com/2.0/branches/{branch_id}/reviews"
        params = {
            'limit': 1,
            'locale': 'ru_RU',
            'fields': 'meta.branch_rating,meta.branch_reviews_count',
            'key': TWO_GIS_API_KEY
        }
        try:
            response = self._session.get(api_url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                meta = data.get('meta', {})
                total_rating = str(meta.get('branch_rating', ''))
                reviews_count = str(meta.get('branch_reviews_count', ''))
                return Rating(
                    source=SourceEnum.TWO_GIS,
                    store=self.current_store,
                    total_rating=total_rating,
                    reviews_count=reviews_count,
                    reviews_regard=reviews_count,
                    date=datetime.now().strftime('%d.%m.%Y')
                )
        except Exception as e:
            print(f"API error for {branch_id}: {e}")
        return Rating(
            source=SourceEnum.TWO_GIS,
            store=self.current_store,
            total_rating='',
            reviews_count='',
            reviews_regard='',
            date=datetime.now().strftime('%d.%m.%Y')
        )

if __name__ == '__main__':  # Удалить!
    obj = TwoGisParser()
    # print(obj.run('https://public-api.reviews.2gis.com/2.0/branches/563478234508453/reviews'))

    # s_obj = TwoGisSeleniumParser()
    #
    # s_obj.run(
    #     'https://2gis.ru/novoaltajsk/branches/563486824415521/firm/563478234508453',
    #     store='Центральный офис'
    # )
