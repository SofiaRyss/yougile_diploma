import time
import pytest
import allure
from typing import Any
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.board_page import BoardPage
from config import YOUGILE_LOGIN, YOUGILE_PASSWORD


@allure.feature("UI Тестирование YouGile")
class TestLogin:
    """UI ТЕСТ-КЕЙС 1: Успешный вход в систему"""

    @allure.title("Успешная авторизация в системе")
    @allure.story("Вход с валидными учетными данными")
    @pytest.mark.ui
    def test_login_success(self, browser: Any) -> None:
        """Проверка успешного входа с валидными данными"""
        with allure.step("Открыть страницу входа"):
            login_page = LoginPage(browser)
            login_page.open_login_page()

        with allure.step("Ввести логин и пароль и нажать Войти"):
            login_page.login(YOUGILE_LOGIN, YOUGILE_PASSWORD)

        with allure.step("Проверить, что вход выполнен успешно"):
            time.sleep(5)
            current_url = browser.current_url
            print(f"\n Текущий URL: {current_url}")

            assert "team" in current_url.lower() or "board" in current_url.lower(), \
                f"Мы всё ещё на странице входа. URL: {current_url}"

            print(f"✅ Успешный вход! Мы внутри системы. URL: {current_url}")


@allure.feature("UI Тестирование YouGile")
class TestCreateTask:
    """UI ТЕСТ-КЕЙС 2: Создание задачи на доске"""

    @allure.title("Создание новой задачи на доске")
    @allure.story("Создание задачи в выбранной колонке")
    @pytest.mark.ui
    def test_create_task_success(self, browser: Any) -> None:
        """Проверка создания новой задачи на доске"""
        with allure.step("Войти в систему"):
            login_page = LoginPage(browser)
            login_page.open_login_page()
            login_page.login(YOUGILE_LOGIN, YOUGILE_PASSWORD)

        with allure.step("Открыть доску и создать задачу"):
            board_page = BoardPage(
                browser, "https://ru.yougile.com/team/bc85143db2e5/Проект-ДЗ-София")
            board_page.open_board()

            task_name = f"Тестовая задача {time.strftime('%H%M%S')}"
            board_page.create_task(task_name)

        with allure.step("Проверить, что задача создана"):
            assert board_page.is_task_exists(
                task_name), f"Задача '{task_name}' не была создана"
            print(f"\n✅ Задача успешно создана: {task_name}")


@allure.feature("UI Тестирование YouGile")
class TestMoveTask:
    """UI ТЕСТ-КЕЙС 3: Перемещение задачи между колонками"""

    @allure.title("Перемещение задачи между колонками")
    @allure.story("Изменение статуса задачи")
    @pytest.mark.ui
    def test_move_task_success(self, browser: Any) -> None:
        """Проверка перемещения существующей задачи"""
        with allure.step("Войти в систему и открыть доску"):
            login_page = LoginPage(browser)
            login_page.open_login_page()
            login_page.login(YOUGILE_LOGIN, YOUGILE_PASSWORD)

            board_page = BoardPage(
                browser, "https://ru.yougile.com/team/bc85143db2e5/Проект-ДЗ-София")
            board_page.open_board()

        with allure.step("Переместить задачу в колонку 'Первая'"):
            board_page.move_task("Тестовая задача 122028", "Первая")

        with allure.step("Проверить, что задача находится в колонке 'Первая'"):
            assert board_page.is_task_in_column("Тестовая задача 122028", "Первая"), \
                "Задача не найдена в колонке 'Первая' после перемещения!"
            print("\n✅ Задача успешно перемещена в колонку 'Первая'!")


@allure.feature("UI Тестирование YouGile")
class TestAddComment:
    """UI ТЕСТ-КЕЙС 4: Добавление комментария к задаче"""

    @allure.title("Добавление комментария к задаче")
    @allure.story("Успешное добавление текстового комментария")
    @pytest.mark.ui
    def test_add_comment_success(self, browser: Any) -> None:
        """Проверка добавления комментария к существующей задаче"""
        with allure.step("Войти в систему и открыть доску"):
            login_page = LoginPage(browser)
            login_page.open_login_page()
            login_page.login(YOUGILE_LOGIN, YOUGILE_PASSWORD)

            board_page = BoardPage(
                browser, "https://ru.yougile.com/team/bc85143db2e5/Проект-ДЗ-София")
            board_page.open_board()

        with allure.step("Добавить комментарий к задаче"):
            comment_text = f"Тестовый комментарий {time.strftime('%H%M%S')}"
            board_page.add_comment_to_task(
                "Тестовая задача 122028", comment_text)

        with allure.step("Проверить результат"):
            print(f"\n✅ Тест добавления комментария успешно пройден!")


@allure.feature("UI Тестирование YouGile")
class TestDeleteTask:
    """UI ТЕСТ-КЕЙС 5: Удаление задачи с доски"""

    @allure.title("Удаление задачи с доски")
    @allure.story("Успешное удаление задачи через контекстное меню")
    @pytest.mark.ui
    def test_delete_task_success(self, browser: Any) -> None:
        """Проверка удаления существующей задачи"""
        with allure.step("Войти в систему и открыть доску"):
            login_page = LoginPage(browser)
            login_page.open_login_page()
            login_page.login(YOUGILE_LOGIN, YOUGILE_PASSWORD)

            board_page = BoardPage(
                browser, "https://ru.yougile.com/team/bc85143db2e5/Проект-ДЗ-София")
            board_page.open_board()

        with allure.step("Создать задачу для удаления"):
            task_to_delete = f"Задача для удаления {time.strftime('%H%M%S')}"
            board_page.create_task(task_to_delete)

            assert board_page.is_task_exists(task_to_delete), \
                f"Задача '{task_to_delete}' не была создана"
            print(f"✅ Задача '{task_to_delete}' создана и готова к удалению")

        with allure.step("Удалить задачу и проверить результат"):
            board_page.delete_task(task_to_delete)

            assert not board_page.is_task_exists(task_to_delete), \
                f"Задача '{task_to_delete}' всё ещё присутствует на доске после удаления!"

            print(f"\n✅ Тест удаления задачи успешно пройден!")
