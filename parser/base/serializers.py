from abc import ABC
from pandas import DataFrame
from parser.base.data_typing import Review, ListedReviews, OfficialAnswer, User, Rating, ListedRating


class SerializerInterface(ABC):
    """
    Базовый интерфейс для преобразования полученных с сайтов данных к единому виду.
    В качестве общего типа используется типизированный словарь Review
    """

    def _serialize_single(self, data: dict) -> Review:
        raise NotImplementedError

    def _serialize_from_list(self, data: list) -> list[Review]:
        raise NotImplementedError

    def serialize(self, data: dict | list[dict]) -> Review | list[Review]:
        raise NotImplementedError


def listed_reviews_serializer(reviews: list[Review]) -> ListedReviews:
    """
    Функция для преобразования списка отзывов в ListedReviews для последующего представления в виде DataFrame
    """
    list_reviews_data: ListedReviews = ListedReviews(
        id=list(),
        text=list(),
        rating=list(),
        date_created=list(),
        provider=list(),
        likes_count=list(),
        comments_count=list(),
        official_answer_id=list(),
        official_answer_org_name=list(),
        official_answer_text=list(),
        official_answer_date_created=list(),
        user_id=list(),
        user_first_name=list(),
        user_last_name=list(),
        user_date_created=list(),
        user_photo_preview_url=list(),
        store=list(),
        reviews_count=list(),
        total_rating=list(),
        reviews_regard=list(),
    )

    for review in reviews:
        list_reviews_data['id'].append(review['id'])
        list_reviews_data['text'].append(review['text'])
        list_reviews_data['rating'].append(review['rating'])
        list_reviews_data['date_created'].append(review['date_created'])
        list_reviews_data['provider'].append(review['provider'])
        list_reviews_data['likes_count'].append(review['likes_count'])
        list_reviews_data['comments_count'].append(review['comments_count'])

        official_answer: OfficialAnswer = review['official_answer']

        list_reviews_data['official_answer_id'].append(official_answer['id'] if official_answer is not None else None)
        list_reviews_data['official_answer_org_name'].append(
            official_answer['org_name'] if official_answer is not None else None)
        list_reviews_data['official_answer_text'].append(
            official_answer['text'] if official_answer is not None else None)
        list_reviews_data['official_answer_date_created'].append(
            official_answer['date_created'] if official_answer is not None else None)

        user: User = review['user']

        list_reviews_data['user_id'].append(user['id'] if user is not None else None)
        list_reviews_data['user_first_name'].append(user['first_name'] if user is not None else None)
        list_reviews_data['user_last_name'].append(user['last_name'] if user is not None else None)
        list_reviews_data['user_date_created'].append(user['date_created'] if user is not None else None)
        list_reviews_data['user_photo_preview_url'].append(user['photo_preview_url'] if user is not None else None)
        list_reviews_data['store'].append(review['store'])
        list_reviews_data['total_rating'].append(review['total_rating'])
        list_reviews_data['reviews_count'].append(review['reviews_count'])
        list_reviews_data['reviews_regard'].append(review['reviews_regard'])

    return list_reviews_data


def data_frame_serializer(reviews: ListedReviews) -> DataFrame:
    """
    Функция для преобразования ListedReviews в Dataframe
    """
    return DataFrame(reviews)


def listed_rating_serializer(ratings: list[Rating]) -> ListedRating:
    listed_rating_data = ListedRating(
        source=list(),
        store=list(),
        total_rating=list(),
        reviews_count=list(),
        reviews_regard=list(),
        date=list(),
    )
    for item in ratings:
        listed_rating_data['source'].append(item.get('source'))
        listed_rating_data['store'].append(item.get('store'))
        listed_rating_data['total_rating'].append(item.get('total_rating'))
        listed_rating_data['reviews_count'].append(item.get('reviews_count'))
        listed_rating_data['reviews_regard'].append(item.get('reviews_regard'))
        listed_rating_data['date'].append(item.get('date'))

    return listed_rating_data