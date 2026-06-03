import traceback

import pandas
from dotenv import find_dotenv, load_dotenv

from parser.constants import SHOP_DATA_FILE_PATH
from parser.enums import SourceEnum
from parser.exc import ErrorDataSerializing
from parser.logging_ import logger
from parser.rating_parser import RatingsSeleniumParser
from parser.utils import time_score_decorator, convert_rating_to_df, save_rating

load_dotenv(find_dotenv())


@time_score_decorator
def pars_ratings() -> None:
    """
    Точка запуска парсинга рейтингов торговых точек
    """
    data = pandas.read_excel(SHOP_DATA_FILE_PATH)

    ratings = list()

    with RatingsSeleniumParser() as parser:
        for idx, row in data.iterrows():
            two_gis_url = row['Ссылка 2ГИС']
            yandex_url = row['Ссылка Яндекс']
            store = row['Магазин']

            try:
                ratings.append(parser.run(url=two_gis_url, store=store, source=SourceEnum.TWO_GIS))
            except ErrorDataSerializing as e:
                logger.debug(e)
                logger.info(f'Error parsing {store} with TWO_GIS\n{two_gis_url}')
            try:
                ratings.append(parser.run(url=yandex_url, store=store, source=SourceEnum.YANDEX))
            except ErrorDataSerializing as e:
                logger.debug(e)
                logger.info(f'Error parsing {store} with YANDEX\n{yandex_url}')

        logger.info(ratings)
        ratings_df = convert_rating_to_df(ratings)
        save_rating(ratings_df)


if __name__ == '__main__':
    try:
        pars_ratings()
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exception(e))
        raise e
