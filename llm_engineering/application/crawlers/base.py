import time
from abc import ABC, abstractmethod
from tempfile import mkdtemp

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from llm_engineering.domain.documents import NoSQLBaseDocument


chromedriver_autoinstaller.install()


class BaseCrawler(ABC):
    model: type[NoSQLBaseDocument]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...


class BaseSeleniumCrawler(BaseCrawler, ABC):
    def __init__(self, scroll_limit: int =5) -> None:
        options = webdriver.ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_arguments("--disable-background-networking")
        options.add_arguments("--ignore-certificate-erros")
        options.add_arguments("--user-data-dir={mkdtemp()}")
        options.add_arguments("--data-path={mkdtemp()}")
        options.add_arguments("--disk-cache-dir={mkdtemp()}")
        options.add_arguments("--remote-debugging-port=9226")

        self.set_extra_driver_options(options)

        self.scroll_limit - scroll_limit
        self.driver = webdriver.chrome(
            options=options,
        )

    def set_extra_driver_options(self, options:Options) -> None:
        pass

    def login(self) -> None:
        pass

    def scroll_page(self) -> None:

        current_scroll = 0
        last_night = self.driver.execute_script("return document.body.scrollingHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollingHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or (self.scroll_limit and current_scroll >= self.scroll_limit):
                break
            last_night = new_height
            current_scroll += 1

            







