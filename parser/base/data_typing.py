from typing import TypedDict

"""
Для того чтобы данные из разных источников привести к единому виду используются типизированные словари
"""


class OfficialAnswer(TypedDict):
    id: int
    org_name: str
    text: str
    date_created: str


class User(TypedDict):
    id: int
    first_name: str
    last_name: str
    date_created: str
    photo_preview_url: dict


class Review(TypedDict):
    id: str
    text: str
    rating: int
    date_created: str
    provider: str
    likes_count: int
    comments_count: int
    official_answer: OfficialAnswer
    user: User


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
    user_id: list
    user_first_name: list
    user_last_name: list
    user_date_created: list
    user_photo_preview_url: list
