from pprint import pprint

from pandas import DataFrame

from parser.constants import RATING_DATA_FRAME_COLUMNS_MAPPING
from parser.two_gis import TwoGisParser
from yandex import YandexParser
from concurrent.futures import ProcessPoolExecutor
import pandas
from datetime import datetime
from parser.base.serializers import listed_reviews_serializer, data_frame_serializer, listed_rating_serializer

from rating_parser import RatingsSeleniumParser


def pars_reviews():
    start = datetime.now()

    data = pandas.read_excel('../Магазины.xlsx')

    reviews = list()

    two_gis_parser = TwoGisParser()
    yandex_parser = YandexParser()

    for idx, row in data.iterrows():
        url = row['Ссылка 2ГИС API']
        store = row['Магазин']
        reviews.extend(two_gis_parser.run(url, store=store))

    for idx, row in data.iterrows():
        url = row['Ссылка Яндекс']
        store = row['Магазин']
        reviews.extend(yandex_parser.run(url, store=store))

    data_frame_serializer(listed_reviews_serializer(reviews)).to_excel('reviews.xlsx', index=False)

    print(datetime.now() - start)


def pars_ratings():
    start = datetime.now()
    data = pandas.read_excel('../Магазины.xlsx')

    two_gis_parser = RatingsSeleniumParser()

    ratings = list()

    for idx, row in data.iterrows():
        url = row['Ссылка 2ГИС']
        store = row['Магазин']
        ratings.append(two_gis_parser.run(url, store=store, source='2ГИС'))

    for idx, row in data.iterrows():
        url = row['Ссылка Яндекс']
        store = row['Магазин']
        ratings.append(two_gis_parser.run(url, store=store, source='Яндекс'))

    two_gis_parser.web_driver.close()

    ratings = listed_rating_serializer(ratings)

    ratings_df = DataFrame(ratings)
    ratings_df.sort_values('store', inplace=True)
    ratings_df = ratings_df.reindex(columns=RATING_DATA_FRAME_COLUMNS_MAPPING)
    ratings_df.rename(columns=RATING_DATA_FRAME_COLUMNS_MAPPING, inplace=True)

    ratings_df.to_excel('Парсинг Рейтингов_.xlsx', index=False)

    print(datetime.now() - start)


if __name__ == '__main__':
    pars_ratings()
