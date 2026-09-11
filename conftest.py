import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Any
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def browser() -> Any:
    """Фикстура для создания браузера"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()
