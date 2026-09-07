from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
from typing import Any
import time


class LoginPage(BasePage):
    """Страница входа в YouGile"""

    LOGIN_URL = "https://ru.yougile.com/team/"

    def __init__(self, driver: Any) -> None:
        super().__init__(driver)

    def open_login_page(self) -> None:
        """Открыть страницу входа"""
        print(f"🌐 Открываем страницу: {self.LOGIN_URL}")
        self.driver.get(self.LOGIN_URL)
        time.sleep(3)

    def login(self, email: str, password: str) -> None:
        """Войти в систему (или пропустить, если уже вошли)"""
        print(f"🔐 Проверяем необходимость входа...")

        # Проверяем, не залогинены ли мы уже (ищем поле email, ждем всего 3 секунды)
        try:
            email_field = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
            )
            print("📝 Поле логина найдено, выполняем вход.")

            ActionChains(self.driver).click(email_field).perform()
            time.sleep(0.5)
            email_field.send_keys(email)
            print("✅ Email введён")

            password_field = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder='Введите пароль'], input[type='password']"))
            )

            ActionChains(self.driver).click(password_field).perform()
            time.sleep(0.5)
            password_field.send_keys(password)
            print("✅ Пароль введён")

            password_field.send_keys(Keys.ENTER)
            print("✅ Enter нажат для входа")

            time.sleep(3)
            print("🎉 Вход выполнен!")

        except TimeoutException:
            # Если поле не найдено за 3 секунды, значит мы уже внутри!
            print("✅ Мы уже авторизованы, пропускаем ввод логина и пароля.")
