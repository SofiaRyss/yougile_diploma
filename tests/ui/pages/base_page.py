from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import Any


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def find_element(self, locator: tuple, timeout: int = 10) -> Any:
        """Найти элемент на странице"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator: tuple, timeout: int = 10) -> list:
        """Найти несколько элементов на странице"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
