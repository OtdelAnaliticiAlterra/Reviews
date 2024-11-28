from idlelib.pyparse import trans
from time import sleep
from selenium.webdriver.common.by import By
from parser.base.parsers import SeleniumParserInterface
from selenium.webdriver import Chrome, ActionChains, Keys


class YandexParser(SeleniumParserInterface):
    pass


def main():
    url = 'https://yandex.ru/maps/org/alterra/1133310706/reviews'

    driver = Chrome()

    driver.get(url)

    sleep(7)

    side_bar = driver.find_element(by=By.XPATH,
                                   value='/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[2]/div[2]/h1')

    buttons = driver.find_elements(By.CLASS_NAME, 'business-review-view__comment-expand')
    for button in buttons:
        driver.execute_script("arguments[0].click();", button)

    # actions = ActionChains(driver)
    #
    # for i in range(20):
    #     actions.send_keys(Keys.END)
    #     side_bar.click()
    #
    #     print(i)
    #
    #     sleep(2)

    sleep(30)


if __name__ == '__main__':
    main()
