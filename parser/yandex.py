import re
from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from parser.base.data_typing import Review
from parser.base.parsers import AbstractParserInterface, ParseSessionInterface
from selenium.webdriver import Chrome, ActionChains, Keys

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json


class YandexParser(AbstractParserInterface, ParseSessionInterface):

    def _serialize(self, data: dict | list) -> Review | list[Review]:
        pass

    def pars(self, url: str) -> list[Review]:
        raise NotImplementedError

    def pars_list(self, urls: list[str]) -> list[Review]:
        raise NotImplementedError

    def run(self, url: str | list[str]) -> list[Review]:
        raise NotImplementedError


def catch_response(driver):
    logs = driver.get_log('performance')
    w_data = []
    print(logs)

    for log in logs:
        # if 'fetchReviews' in str(log):
        #     message = json.loads(log['message'])
        #     print(message)
            # w_data.append(message)
    # with open('yandex_log.json', 'w') as file:
    #     json.dump(logs, file)
        if 'fetchReviews' in str(log):
            message = json.loads(log['message'])
            # if message['message']['method'] == 'Network.responseReceived':
            data = message['message']
            print(data)


class COptions(Options):
    @property
    def default_capabilities(self) -> dict:
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        return caps.copy()


def main():
    url = 'https://yandex.ru/maps/org/alterra/1133310706/reviews'

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    options = COptions()

    driver = Chrome(options=options)

    driver.get(url)

    sleep(3)

    pattern = r'(Отзывы. [\d]*)'

    find = re.search(pattern, driver.page_source)

    reviews_count = int(find.group(0).split(' ')[-1])

    title = driver.find_element(By.TAG_NAME, 'h1')
    body = driver.find_element(By.TAG_NAME, 'body')
    actions = ActionChains(driver)

    actions.move_by_offset(*title.location.values())
    actions.click().perform()

    reviews = driver.find_elements(By.CLASS_NAME, 'business-reviews-card-view__review')

    while len(reviews) < reviews_count:
        body.send_keys(Keys.END)
        sleep(1)
        reviews = driver.find_elements(By.CLASS_NAME, 'business-reviews-card-view__review')

    catch_response(driver)

    print(len(reviews))

    sleep(30)
    driver.quit()


if __name__ == '__main__':
    main()
