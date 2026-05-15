import os
from datetime import datetime
from functools import wraps
import pandas
from pandas import DataFrame, Series

from parser.base.data_typing import Rating
from parser.base.serializers import listed_rating_serializer
from parser.constants import RATING_DATA_FRAME_COLUMNS_MAPPING, RATING_FILE_NAME, MARKETING_FOLDER_PATH


def time_score_decorator(func: callable) -> callable:
    """
    Декоратор для подсчета времени работы функции
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        print(f'---------- <{func.__name__}> ----------')
        func(*args, **kwargs)
        print(datetime.now() - start)

    return wrapper


def convert_rating_to_df(ratings: list[Rating]) -> DataFrame:
    """
    Функция для конвертации списка рейтингов в DataFrame
    """
    ratings = listed_rating_serializer(ratings)

    ratings_df = DataFrame(ratings)
    ratings_df.sort_values('store', inplace=True)
    ratings_df = ratings_df.reindex(columns=RATING_DATA_FRAME_COLUMNS_MAPPING)
    ratings_df.rename(columns=RATING_DATA_FRAME_COLUMNS_MAPPING, inplace=True)

    return ratings_df


def normalize_dtype_date_column(row: Series) -> datetime:
    """
    Функция для приведения даты в итоговом DataFrame к единому виду.
    Что позволяет корректно отсортировать DataFrame по дате
    """
    if isinstance(row['Дата'], str):
        return datetime.strptime(row['Дата'], '%d.%m.%Y')
    else:
        return row['Дата']


def save_rating(ratings_data: DataFrame) -> None:
    """
    Сохранение итогового DataFrame в Excel файл.
    В данном случае сохранение производится в директорию для Bi отчета
    """
    file_path = os.path.join(MARKETING_FOLDER_PATH, RATING_FILE_NAME)
    if os.path.exists(file_path):
        file_data = pandas.read_excel(file_path)
        result_data = pandas.concat([file_data, ratings_data], ignore_index=True)
    else:
        result_data = ratings_data
    file_data = pandas.read_excel(file_path)

    result_data = pandas.concat([file_data, ratings_data], ignore_index=True)
    result_data['Дата'] = result_data['Дата'].convert_dtypes(convert_string=True)
    result_data['Дата'] = result_data.apply(normalize_dtype_date_column, axis=1)
    result_data.sort_values('Дата', ascending=False, inplace=True)
    result_data['Дата'] = result_data['Дата'].apply(datetime.strftime, args=('%d.%m.%Y',))

    # result_data.to_excel(str(RATING_FILE_NAME), index=False)
    result_data.to_excel(str(file_path), index=False)
