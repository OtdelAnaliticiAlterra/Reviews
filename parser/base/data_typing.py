from typing import TypedDict

"""
Для того чтобы данные из разных источников привести к единому виду используются типизированные словари
"""


class OfficialAnswer(TypedDict):
    """
    Типизированный словарь официальных ответов на отзывы использующийся как единое
    представление полученных с сайтов данных
    """
    id: int
    org_name: str
    text: str
    date_created: str


class User(TypedDict):
    """
    Типизированный словарь пользователей использующийся как единое представление полученных с сайтов данных
    """
    id: int | None
    first_name: str | None
    last_name: str | None
    date_created: str | None
    photo_preview_url: dict | None


class Review(TypedDict):
    """
    Типизированный словарь отзывов использующийся как единое представление полученных с сайтов данных
    """
    id: str | None
    text: str
    rating: int
    date_created: str
    provider: str
    likes_count: int
    comments_count: int | None
    official_answer: OfficialAnswer | None
    user: User

    store: str | None  # Наш магазин
    total_rating: str | float | None
    reviews_count: str | int | None

    reviews_regard: str | int | None  # Количество оценок (количество человек оставивших оценку рейтинга звездами)


class ListedReviews(TypedDict):
    """
    Словарь заполняемый горизонтально, для последующего преобразования в DataFrame
    """
    id: list
    text: list
    rating: list
    date_created: list
    provider: list
    likes_count: list
    comments_count: list

    official_answer_id: list
    official_answer_org_name: list
    official_answer_text: list
    official_answer_date_created: list

    user_id: list
    user_first_name: list
    user_last_name: list
    user_date_created: list
    user_photo_preview_url: list
    store: list  # Наш магазин
    total_rating: list
    reviews_count: list  # Количество оставленных отзывов
    reviews_regard: list  # Количество оценок (количество человек оставивших оценку рейтинга звездами)


class Rating(TypedDict):
    """
    Словарь рейтингов
    """
    source: str
    store: str
    total_rating: str
    reviews_count: str
    reviews_regard: str
    date:str


class ListedRating(TypedDict):
    """
    Словарь заполняемый горизонтально, для последующего преобразования в DataFrame
    """
    source: list
    store: list
    total_rating: list
    reviews_count: list
    reviews_regard: list
    date: list
