import pytest
import allure
from utils.api_client import ApiClient
from data.user_data import generate_user

# Глобальный клиент, доступный во всех тестах
@pytest.fixture(scope="session")
def client():
    return ApiClient()

# Фикстура создания пользователя с логами для Allure
@pytest.fixture
def registered_user(client):
    user = generate_user()

    with allure.step("Создание пользователя через API"):
        response = client.create_user(user)
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
        allure.attach(str(response.json()), name="User creation response", attachment_type=allure.attachment_type.JSON)

    return user
