import pytest
import allure
from utils.api_client import ApiClient
from data.user_data import generate_user

client = ApiClient()

VALID_INGREDIENTS = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa75"]
INVALID_INGREDIENTS = ["invalid_hash"]

@pytest.fixture
def auth_token():
    user = generate_user()
    client.create_user(user)
    login = client.login_user(user)
    return login.json()["accessToken"].split("Bearer ")[-1]

@allure.epic("Создание заказа")
@allure.feature("Заказ с ингредиентами")
class TestOrderCreation:

    @allure.story("Создание заказа с валидными ингредиентами и авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание заказа с валидными ингредиентами и авторизацией")
    def test_create_order_with_auth_and_ingredients(self, auth_token):
        with allure.step("Отправляем запрос на создание заказа с валидными ингредиентами и авторизацией"):
            response = client.create_order(VALID_INGREDIENTS, auth_token)

        with allure.step("Проверяем, что заказ был создан, и ингредиенты присутствуют"):
            assert response.status_code == 200, f"Ожидался статус 200, но получили {response.status_code}"
            assert response.json()["order"]["ingredients"] is not None, "Ингредиенты должны быть, но их нет"
            allure.attach(str(response.json()), name="Ответ на заказ", attachment_type=allure.attachment_type.JSON)

    @allure.story("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        with allure.step("Отправляем запрос на создание заказа без авторизации"):
            response = client.create_order(VALID_INGREDIENTS)

        with allure.step("Проверяем, что заказ был создан, даже без авторизации"):
            assert response.status_code == 200, f"Ожидался статус 200, но получили {response.status_code}"

    @allure.story("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, auth_token):
        with allure.step("Отправляем запрос на создание заказа без ингредиентов"):
            response = client.create_order([], auth_token)

        with allure.step("Проверяем, что заказ не может быть создан без ингредиентов"):
            assert response.status_code == 400, f"Ожидался статус 400, но получили {response.status_code}"
            assert response.json()["message"] == "Ingredient ids must be provided", "Сообщение об ошибке неверно"

    @allure.story("Создание заказа с неверными ингредиентами")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание заказа с неверными ингредиентами")
    def test_create_order_with_invalid_ingredients(self, auth_token):
        with allure.step("Отправляем запрос на создание заказа с неверными ингредиентами"):
            response = client.create_order(INVALID_INGREDIENTS, auth_token)

        with allure.step("Проверяем, что заказ не может быть создан с неверными ингредиентами"):
            assert response.status_code == 500 or response.status_code == 400, \
                f"Ожидался статус 500 или 400, но получили {response.status_code}"
            allure.attach(str(response.json()), name="Ошибка с неверными ингредиентами", attachment_type=allure.attachment_type.JSON)
