from enum import Enum

from requests import Response

from parser.base.parsers import ParseSessionInterface, AbstractRequestsParser
from parser.base.serializers import SerializerInterface
from parser.base.data_typing import Review, User, OfficialAnswer


class SerializeModeEnum(Enum):
    SOFT: str = 'SOFT'
    HARD: str = 'HARD'


class TwoGisSerializer(SerializerInterface):

    def __init__(self, mode: SerializeModeEnum):
        self.__mode = mode

    def __user_serializer(self, data: dict) -> User | None:
        if data is None: return None

        user: User = {
            field: data.get(field)
            for field in User.__annotations__.keys()
        }
        return User(**user)

    def __official_answer_serializer(self, data: dict) -> OfficialAnswer | None:
        if data is None: return None

        official_answer: OfficialAnswer = {
            field: data.get(field)
            for field in OfficialAnswer.__annotations__.keys()
        }
        return OfficialAnswer(**official_answer)

    def _serialize_single(self, data: dict) -> Review:
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
        reviews: list[Review] = list()
        for review in data:
            reviews.append(self._serialize_single(review))
        return reviews

    def serialize(self, data: dict | list) -> Review | list[Review]:
        if isinstance(data, list):
            return self._serialize_from_list(data)
        elif isinstance(data, dict):
            return self._serialize_single(data)
        else:
            raise ValueError(f'Type {type(data)} is not serializable')


class TwoGisParser(AbstractRequestsParser, ParseSessionInterface):
    BASE_URL: str = 'https://public-api.reviews.2gis.com/2.0/branches/563478234508453/reviews'

    HEADERS: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    BASE_PARAMS: dict = {
        'limit': '50',
        'locale': 'ru_RU',
        'sort_by': 'date_created',

        'key': 'b0209295-ae15-48b2-acb2-58309b333c37',
    }

    def __init__(self):
        super().__init__()
        self._serializer = TwoGisSerializer(mode=SerializeModeEnum.SOFT)

    def _serialize(self, data: dict | list) -> Review | list[Review]:
        return self._serializer.serialize(data)

    def run(self) -> list[Review]:
        reviews: list = list()

        next_link = self.BASE_URL

        while next_link is not None:
            response: Response = self._session.get(next_link, params=self._params)

            reviews.extend(response.json().get('reviews'))
            next_link = response.json().get('next_link')

        return self._serialize(reviews)


p_obj = TwoGisParser()

data = p_obj.run()
print(data)
