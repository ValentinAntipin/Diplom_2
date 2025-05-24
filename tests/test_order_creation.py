import pytest
import allure
from conftest import VALID_INGREDIENTS, INVALID_INGREDIENTS
from data.response_messages import INGREDIENTS_REQUIRED_ERROR, INVALID_INGREDIENTS_ERROR


@allure.epic("Создание заказа")
@allure.feature("Заказ с ингредиентами")
class TestOrderCreation:

    @allure.story("Создание заказа с валидными ингредиентами и авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание заказа с валидными ингредиентами и авторизацией")
    def test_create_order_with_auth_and_ingredients(self, client, auth_token):
        with allure.step("Отправляем запрос на создание заказа с валидными ингредиентами и авторизацией"):
            response = client.create_order(VALID_INGREDIENTS, auth_token)
            data = response.json()

        with allure.step("Проверяем, что заказ был успешно создан"):
            assert response.status_code == 200
            assert data.get("success") is True
            assert data.get("order") is not None
            assert data["order"].get("ingredients") is not None
            assert isinstance(data["order"]["ingredients"], list)
            allure.attach(str(data), name="Ответ на заказ", attachment_type=allure.attachment_type.JSON)

    @allure.story("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, client):
        with allure.step("Отправляем запрос на создание заказа без авторизации"):
            response = client.create_order(VALID_INGREDIENTS)
            data = response.json()

        with allure.step("Проверяем, что заказ был создан без авторизации"):
            assert response.status_code == 200
            assert data.get("success") is True
            assert data.get("order") is not None
            allure.attach(str(data), name="Ответ без авторизации", attachment_type=allure.attachment_type.JSON)

    @allure.story("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, client, auth_token):
        with allure.step("Отправляем запрос на создание заказа без ингредиентов"):
            response = client.create_order([], auth_token)
            data = response.json()

        with allure.step("Проверяем корректную обработку ошибки"):
            assert response.status_code == 400
            assert data.get("message") == INGREDIENTS_REQUIRED_ERROR
            allure.attach(str(data), name="Ошибка без ингредиентов", attachment_type=allure.attachment_type.JSON)

    @allure.story("Создание заказа с неверными ингредиентами")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание заказа с неверными ингредиентами")
    def test_create_order_with_invalid_ingredients(self, client, auth_token):
        with allure.step("Отправка запроса на создание заказа с неверными ингредиентами"):
            response = client.create_order(INVALID_INGREDIENTS, auth_token)
            try:
                data = response.json()
            except Exception as e:
                pytest.fail(f"Не удалось распарсить JSON из ответа сервера: {e}")

        with allure.step("Проверка, что заказ не создаётся и возвращается ошибка"):
            assert response.status_code in [400, 500]
            assert data.get("message") == INVALID_INGREDIENTS_ERROR
            allure.attach(str(data), name="Ошибка с неверными ингредиентами",
                          attachment_type=allure.attachment_type.JSON)
