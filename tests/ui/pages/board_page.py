"""Страница доски задач YouGile."""

from typing import Any
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage


class BoardPage(BasePage):
    """Page Object для доски задач YouGile."""

    def __init__(self, driver: WebDriver, board_url: str) -> None:
        """Инициализация страницы доски."""
        super().__init__(driver)
        self.board_url = board_url

    def open_board(self) -> None:
        """Открыть доску задач."""
        self.driver.get(self.board_url)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Добавить задачу')]")
            )
        )

    def create_task(self, task_name: str) -> None:
        """Создать новую задачу на доске."""
        # Находим поле ввода задачи
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Добавить задачу')]")
            )
        )
        self.driver.execute_script("arguments[0].click();", input_field)

        # Вводим название задачи
        text_area = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "textarea")
            )
        )
        text_area.send_keys(task_name)
        text_area.send_keys(Keys.ENTER)

        # Ждём появления задачи на доске
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{task_name}')]")
            )
        )

    def is_task_exists(self, task_name: str) -> bool:
        """Проверить существование задачи на доске."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//*[contains(text(), '{task_name}')]")
                )
            )
            return True
        except Exception:
            return False

    def is_task_in_column(
        self, task_name: str, column_name: str
    ) -> bool:
        """Проверить, что задача находится в указанной колонке."""
        try:
            xpath = (
                f"//*[contains(text(), '{column_name}')]"
                f"/ancestor::div[contains(@class, 'column') or "
                f"contains(@class, 'board')][1]"
                f"//*[contains(text(), '{task_name}')]"
            )
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except Exception:
            return False

    def move_task(
        self, task_name: str, target_column_name: str
    ) -> None:
        """Переместить задачу в другую колонку."""
        # Открываем карточку задачи
        task_card = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(text(), '{task_name}')]")
            )
        )
        self.driver.execute_script("arguments[0].click();", task_card)

        # Открываем вкладку Инфо
        info_tab = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Инфо')]")
            )
        )
        self.driver.execute_script("arguments[0].click();", info_tab)

        # Нажимаем кнопку перемещения
        move_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.task-info__move-to-board")
            )
        )
        self.driver.execute_script("arguments[0].click();", move_button)

        # Выбираем целевую колонку
        target_column = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(text(), '{target_column_name}')]")
            )
        )
        self.driver.execute_script("arguments[0].click();", target_column)

        # Закрываем карточку
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def add_comment_to_task(
        self, task_name: str, comment_text: str
    ) -> None:
        """Добавить комментарий к задаче."""
        # Открываем карточку задачи
        task_card = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(text(), '{task_name}')]")
            )
        )
        self.driver.execute_script("arguments[0].click();", task_card)

        # Открываем вкладку Чат
        chat_tab = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Чат')]")
            )
        )
        self.driver.execute_script("arguments[0].click();", chat_tab)

        # Вводим комментарий
        comment_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ck-editor__editable_inline")
            )
        )
        self.driver.execute_script(
            """
            arguments[0].innerHTML = arguments[1];
            arguments[0].dispatchEvent(
                new Event('input', {bubbles: true})
            );
            """,
            comment_input,
            comment_text,
        )

        # Нажимаем Enter для отправки
        comment_input.send_keys(Keys.ENTER)

        # Закрываем карточку
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def delete_task(self, task_name: str) -> None:
        """Удалить задачу с доски."""
        # Находим карточку задачи
        task_card = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{task_name}')]")
            )
        )

        # Наводим курсор для появления меню
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).move_to_element(task_card).perform()

        # Открываем меню задачи
        menu_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-testid='board-task-menu']")
            )
        )
        self.driver.execute_script("arguments[0].click();", menu_button)

        # Выбираем пункт "Удалить"
        delete_item = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-testid='menu-item-delete']")
            )
        )
        self.driver.execute_script("arguments[0].click();", delete_item)

        # Подтверждаем удаление через Enter (модальное окно)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)

        # Ждём исчезновения задачи
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{task_name}')]")
            )
        )
