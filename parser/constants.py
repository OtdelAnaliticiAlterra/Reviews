from pathlib import Path
import os

# Рейтинг
TWO_GIS_TOTAL_RATING_XPATH_LIST = [
    '//*[@id="root"]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[4]/div/div[2]',
    '//*[@id="root"]/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[5]/div/div[2]',
    '/html/body/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[4]/div/div[2]',
]
TWO_GIS_REVIEWS_REGARD_XPATH = [
    '//*[@id="root"]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[4]/div/div[3]',
    '//*[@id="root"]/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[5]/div/div[3]',
    '/html/body/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div[2]',
    '/html/body/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[4]/div/div[3]',
]
TWO_GIS_REVIEWS_COUNT_XPATH = [
    '//*[@id="root"]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div[1]/div[3]/h2/a/span',
    '//*[@id="root"]/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div[1]/div[3]/h2/a/span',
    '/html/body/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div[1]/div[3]/h2/a/span',
    '/html/body/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div[3]/h2/a/span',
    '/html/body/div[2]/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div[3]/h2/a/span',
]

# Рейтинг
YANDEX_TOTAL_RATING_XPATH_LIST = [
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[7]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
    '/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[5]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
    '/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[6]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
    '/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[5]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[6]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
    '/html/body/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[4]/div/div[2]',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[6]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[6]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]',
]

# Кол-во оценок
YANDEX_REVIEWS_REGARD_XPATH = [
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[7]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[6]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span',
    '/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[5]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span',
    '/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[6]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span',
    '/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[5]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[6]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/span',
]

# Кол-во отзывов
YANDEX_REVIEWS_COUNT_XPATH = [
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[2]/div[2]/div/div/div/div[1]/div[4]/div/div',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[2]/div[2]/div/div/div/div[1]/div[5]/div/div',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/div/div/div/div[1]/div[4]/div/div',
    '/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[2]/div[2]/div/div/div/div[1]/div[3]/div/div',
    '/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/div/div/div/div[1]/div[3]/div/div',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/div/div/div/div[1]/div[3]/div/div',
    '/html/body/div[1]/div[2]/div[8]/aside/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[2]/div[2]/div/div/div/div[1]/div[3]/div/div',
]

RATING_DATA_FRAME_COLUMNS_MAPPING = {
    'store': 'Магазин',
    'total_rating': 'Рейтинг',
    'reviews_regard': 'Оценки',
    'reviews_count': 'Отзывы',
    'source': 'Источник',
    'date': 'Дата',
}

BASE_DIR = Path(__file__).resolve().parent.parent

MARKETING_FOLDER_PATH = '\\\\tg-storage01\\Маркетинг\\Общие\\Отдел аналитики\\Рейтинги Альтерра'
# MARKETING_FOLDER_PATH = 'C:\\Users\\Analiticscript\\Projects\\Reviews'

SHOP_DATA_FILE_PATH = os.path.join(BASE_DIR, 'Магазины.xlsx')

RATING_FILE_NAME = 'Парсинг Рейтингов.xlsx'

CHATS_IDS = '\\\\TG-Storage01\\Аналитический отдел\\Проекты\\Python\\chats_ids.csv'
