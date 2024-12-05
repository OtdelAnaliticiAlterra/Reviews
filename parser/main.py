from parser.constants import SHOP_DATA_FILE_PATH
from parser.enums import SourceEnum
from parser.two_gis import TwoGisParser
from parser.utils import time_score_decorator, convert_rating_to_df, save_rating
from yandex import YandexParser
import pandas
from datetime import datetime
from parser.base.serializers import listed_reviews_serializer, data_frame_serializer

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


@time_score_decorator
def pars_ratings() -> None:
    data = pandas.read_excel(SHOP_DATA_FILE_PATH)

    ratings = list()

    with RatingsSeleniumParser() as parser:
        for idx, row in data.iterrows():
            two_gis_url = row['Ссылка 2ГИС']
            yandex_url = row['Ссылка Яндекс']
            store = row['Магазин']
            ratings.append(parser.run(url=two_gis_url, store=store, source=SourceEnum.TWO_GIS))
            ratings.append(parser.run(url=yandex_url, store=store, source=SourceEnum.YANDEX))

        print(ratings)
        ratings_df = convert_rating_to_df(ratings)
        save_rating(ratings_df)


if __name__ == '__main__':
    pars_ratings()
