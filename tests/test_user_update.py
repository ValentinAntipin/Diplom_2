import pytest
import allure
from utils.api_client import ApiClient
from data.user_data import generate_user

client = ApiClient()


@pytest.fixture
def auth_token_and_user():
    user = generate_user()
    client.create_user(user)
    login_response = client.login_user(user)
    token = login_response.json()["accessToken"].split("Bearer ")[-1]
    return token, user


@allure.epic("Управление пользователями")
@allure.feature("Обновление данных пользователя")
class TestUserUpdate:

    @allure.story("Обновление данных авторизованного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Авторизованный пользователь должен иметь возможность обновить свои данные")
    def test_update_user_authorized(self, auth_token_and_user):
        token, _ = auth_token_and_user
        new_data = {"name": "Обновлённое имя"}

        with allure.step("Отправка запроса на обновление данных пользователя с токеном"):
            response = client.update_user(token, new_data)

        with allure.step("Проверка, что получен статус 200 и имя пользователя обновлено"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
            updated_name = response.json()["user"]["name"]
            assert updated_name == "Обновлённое имя", f"Имя пользователя не обновилось: {updated_name}"
            allure.attach(str(response.json()), name="Обновлённые данные пользователя", attachment_type=allure.attachment_type.JSON)

    @allure.story("Попытка обновления данных без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Неавторизованный пользователь не должен иметь возможность обновлять данные")
    def test_update_user_unauthorized(self):
        new_data = {"name": "Взломщик"}

        with allure.step("Отправка запроса на обновление данных без токена авторизации"):
            response = client.update_user("", new_data)

        with allure.step("Проверка, что возвращён статус 401 и сообщение требует авторизации"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
            message = response.json().get("message")
            assert message == "You should be authorised", f"Неожиданное сообщение об ошибке: {message}"
            allure.attach(str(response.json()), name="Ошибка авторизации", attachment_type=allure.attachment_type.JSON)
