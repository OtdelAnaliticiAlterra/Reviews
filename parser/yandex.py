import re
from time import sleep

from selenium.common import NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from parser.base.data_typing import Review, User
from parser.base.parsers import AbstractSeleniumParser, ParseSessionInterface
from selenium.webdriver import ActionChains, Keys

from parser.base.serializers import SerializerInterface


class YandexSerializer(SerializerInterface):

    def _serialize_single(self, data: dict) -> Review:
        return Review(
            id=None,
            provider='yandex',
            text=data['review_text'],
            user=User(
                id=None,
                first_name=data['author_name'],
                last_name=None,
                photo_preview_url=data['author_icon'],
                date_created=None,
            ),
            likes_count=data['review_reaction'],
            date_created=data['date'],
            rating=data['rate_value'],
            official_answer=None,
            comments_count=None,
            store=data['store'],
            total_rating=data['total_rating'],
            reviews_count=data['reviews_count'],
            reviews_regard=data['reviews_regard'],
        )

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


class YandexParser(AbstractSeleniumParser, ParseSessionInterface):

    def __init__(self):
        super().__init__()
        self._serializer = YandexSerializer()

        self.current_store: str | None = None

        self.current_rating_data: dict = dict()
        """
        current_rating_data structure
            'total_rating': 'str',
            'reviews_count': 'str',
            'store': 'str',
            'reviews_regard': 'str',
        """

    def _serialize(self, data: dict | list) -> Review | list[Review]:
        return self._serializer.serialize(data)

    def __load_all_reviews(self, url) -> list[WebElement]:

        pattern = r'(Отзывы. [\d]*)'

        find = re.search(pattern, self.web_driver.page_source)

        reviews_count = int(find.group(0).split(' ')[-1])

        self.current_rating_data.update({'reviews_regard': reviews_count})

        title = self.web_driver.find_element(By.TAG_NAME, 'h1')
        body = self.web_driver.find_element(By.TAG_NAME, 'body')
        actions = ActionChains(self.web_driver)

        actions.move_by_offset(*title.location.values())
        reviews = self.web_driver.find_elements(By.CLASS_NAME, 'business-reviews-card-view__review')

        try:
            actions.click().perform()
            scroll_count = 0
            while len(reviews) < reviews_count:
                body.send_keys(Keys.END)
                sleep(1)
                reviews = self.web_driver.find_elements(By.CLASS_NAME, 'business-reviews-card-view__review')
                scroll_count += 1

                if scroll_count > 40:
                    break

        except MoveTargetOutOfBoundsException:
            print(url)
            print(self.current_store)

        return reviews

    @staticmethod
    def __clean_icon_url(style_data: str) -> str | None:
        if style_data is None:
            return None
        else:
            try:

                icon_url_pattern = r'(https:\/\/avatars\.mds\.yandex\.net\/get-yapic\/[\d]*\/.*\/islands-68)'
                find = re.search(icon_url_pattern, style_data)
                return find.group(0)
            except AttributeError:
                return None

    @staticmethod
    def __get_review_count_reaction(element: WebElement) -> str | None:
        try:
            review_reaction_container = element.find_elements(By.CLASS_NAME, 'business-reactions-view__container')[0]
            return review_reaction_container.find_element(By.CLASS_NAME, 'business-reactions-view__counter').text
        except NoSuchElementException:
            print('not found review count reaction')
            return None

    def get_review_data(self, data: WebElement) -> dict:
        try:
            name = data.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]')
            review_text = data.find_element(By.CLASS_NAME, 'business-review-view__body-text')
            user_icon = data.find_element(By.CLASS_NAME, 'user-icon-view__icon')
            date = data.find_element(By.CSS_SELECTOR, 'meta[itemprop="datePublished"]')
            rate_value = data.find_element(By.CSS_SELECTOR, 'meta[itemprop="ratingValue"]')
        except NoSuchElementException:
            name = None
            review_text = None
            user_icon = None
            date = None
            rate_value = None

        review_reaction: str = self.__get_review_count_reaction(data)

        data_dict = {
            'author_name': name.text if name is not None else None,
            'review_text': review_text.text if review_text is not None else None,
            'author_icon': self.__clean_icon_url(user_icon.get_attribute('style')) if user_icon is not None else None,
            'date': date.get_attribute('content') if date is not None else None,
            'rate_value': rate_value.get_attribute('content') if rate_value is not None else None,
            'review_reaction': review_reaction,
        }

        data_dict.update(self.current_rating_data)

        return data_dict

    def pars(self, url: str) -> list[Review]:

        self.web_driver.get(url)
        sleep(5)

        self.get_rating()

        reviews_web_elements = self.__load_all_reviews(url)

        reviews_data: list = list()

        for web_element in reviews_web_elements:
            reviews = self.get_review_data(web_element)
            reviews_data.append(reviews)

        return self._serialize(reviews_data)

    def pars_list(self, urls: list[str]) -> list[Review]:
        reviews: list = list()
        for url in urls:
            reviews.extend(self.pars(url))
        return reviews

    def run(self, url: str | list[str], store: str = None) -> list[Review]:

        self.current_store = store

        if isinstance(url, str):
            return self.pars(url)
        elif isinstance(url, list):
            return self.pars_list(url)

        self.web_driver.quit()

    def get_rating(self):
        try:
            rating = self.web_driver.find_element(By.CLASS_NAME, 'business-summary-rating-badge-view__rating')
            rating_reviews_count = self.web_driver.find_element(By.CLASS_NAME, 'business-rating-amount-view')
        except NoSuchElementException:
            rating = None
            rating_reviews_count = None

        self.current_rating_data = {
            'total_rating': self.clean_total_rating(rating.text) if rating is not None else None,
            'reviews_count': self.clean_reviews_count(
                rating_reviews_count.text) if rating_reviews_count is not None else None,
            'store': self.current_store,
        }

    @staticmethod
    def clean_total_rating(rating: str) -> str:
        return rating.split(' ')[-1].strip()

    @staticmethod
    def clean_reviews_count(reviews_count: str) -> str:
        return reviews_count.split(' ')[0]


if __name__ == '__main__':
    obj = YandexParser()
    result = obj.run('https://yandex.ru/maps/org/alterra/4300877340/reviews', store='ABC')
    # result = obj.run('https://yandex.ru/maps/org/alterra/130943789947/reviews', store='ABC')
    print(result)
    print(len(result))
    # main()
