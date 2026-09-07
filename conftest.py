import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Any


@pytest.fixture(scope="session")
def browser() -> Any:
    """Фикстура для создания браузера"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()
