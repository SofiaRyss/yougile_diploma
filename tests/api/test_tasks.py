import requests
import pytest
import allure
from config import YOUGILE_API_TOKEN


@allure.feature("API Тестирование YouGile")
class TestTasksAPI:
    """API ТЕСТЫ для работы с задачами YouGile"""

    BASE_URL = "https://yougile.com/api-v2"

    def _get_headers(self) -> dict:
        """Получить заголовки для запросов"""
        return {
            "Authorization": f"Bearer {YOUGILE_API_TOKEN}",
            "Content-Type": "application/json"
        }

    @allure.title("Получение списка досок")
    @allure.story("Успешное получение списка проектов/досок")
    @pytest.mark.api
    def test_get_tasks(self) -> None:
        """API ТЕСТ-КЕЙС 1: Получение списка досок (позитивный)"""
        response = requests.get(
            f"{self.BASE_URL}/boards",
            headers=self._get_headers()
        )
        assert response.status_code == 200, (
            f"Ожидался 200, получен {response.status_code}: "
            f"{response.text}"
        )
        print("✅ API ТЕСТ-КЕЙС 1 пройден: Получение списка досок")

    @allure.title("Создание задачи через API")
    @allure.story("Успешное создание новой задачи")
    @pytest.mark.api
    def test_create_task(self) -> None:
        """API ТЕСТ-КЕЙС 2: Создание задачи через API (позитивный)"""
        task_data = {"title": "Тестовая задача для диплома"}
        response = requests.post(
            f"{self.BASE_URL}/tasks",
            headers=self._get_headers(),
            json=task_data
        )
        assert response.status_code in [200, 201], (
            f"Ожидался 200/201, получен "
            f"{response.status_code}: {response.text}"
        )
        print("✅ API ТЕСТ-КЕЙС 2 пройден: Создание задачи через API")

    @allure.title("Получение информации о задаче")
    @allure.story("Успешное получение данных о существующей задаче")
    @pytest.mark.api
    def test_get_task_by_id(self) -> None:
        """API ТЕСТ-КЕЙС 3: Получение информации о задаче (позитивный)"""
        task_data = {"title": "Задача для получения информации"}
        create_response = requests.post(
            f"{self.BASE_URL}/tasks",
            headers=self._get_headers(),
            json=task_data
        )

        if create_response.status_code in [200, 201]:
            task_id = create_response.json().get("id")
            if task_id:
                response = requests.get(
                    f"{self.BASE_URL}/tasks/{task_id}",
                    headers=self._get_headers()
                )
                assert response.status_code == 200, (
                    f"Ожидался 200, получен "
                    f"{response.status_code}: {response.text}"
                )
                print("✅ API ТЕСТ-КЕЙС 3 пройден: Получение информации о задаче")

    @allure.title("Создание задачи без обязательных полей")
    @allure.story("Ошибка при создании задачи без обязательных полей")
    @pytest.mark.api
    def test_create_task_without_required_fields(self) -> None:
        """API ТЕСТ-КЕЙС 4: Создание без обязательных полей (негативный)"""
        task_data = {}
        response = requests.post(
            f"{self.BASE_URL}/tasks",
            headers=self._get_headers(),
            json=task_data
        )
        assert response.status_code in [400, 422], (
            f"Ожидался 400/422, получен "
            f"{response.status_code}: {response.text}"
        )
        print("✅ API ТЕСТ-КЕЙС 4 пройден: Создание задачи без обязательных полей")

    @allure.title("Доступ к несуществующей задаче")
    @allure.story("Ошибка при получении несуществующей задачи")
    @pytest.mark.api
    def test_get_nonexistent_task(self) -> None:
        """API ТЕСТ-КЕЙС 5: Доступ к несуществующей задаче (негативный)"""
        fake_task_id = "00000000-0000-0000-0000-000000000000"
        response = requests.get(
            f"{self.BASE_URL}/tasks/{fake_task_id}",
            headers=self._get_headers()
        )
        assert response.status_code == 404, (
            f"Ожидался 404, получен "
            f"{response.status_code}: {response.text}"
        )
        print("✅ API ТЕСТ-КЕЙС 5 пройден: Доступ к несуществующей задаче")
