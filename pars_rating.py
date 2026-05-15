import os

import pandas
from dotenv import find_dotenv, load_dotenv
from telegram_bot_logger import TgLogger

from parser.constants import SHOP_DATA_FILE_PATH, CHATS_IDS
from parser.enums import SourceEnum
from parser.rating_parser import RatingsSeleniumParser
from parser.utils import time_score_decorator, convert_rating_to_df, save_rating

load_dotenv(find_dotenv())

logger = TgLogger(
    name='Парсинг Рейтингов',
    token=os.environ.get('LOGGER_BOT_TOKEN'),
    chats_ids_filename=CHATS_IDS,
    file=__file__,
)


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
            ratings.append(parser.run(url=two_gis_url, store=store, source=SourceEnum.TWO_GIS))
            ratings.append(parser.run(url=yandex_url, store=store, source=SourceEnum.YANDEX))

        print(ratings)
        ratings_df = convert_rating_to_df(ratings)
        save_rating(ratings_df)


if __name__ == '__main__':
    try:
        pars_ratings()
    except Exception as e:
        #logger.error(e)
        raise e
