import pytest
import allure


@allure.epic("Аутентификация пользователей")
@allure.feature("Вход в систему")
class TestUserLogin:

    @allure.story("Вход с валидными учетными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Вход существующего пользователя должен возвращать токен доступа")
    def test_login_existing_user(self, registered_user, client):
        with allure.step("Отправка запроса на вход с корректными учетными данными"):
            response = client.login_user(registered_user)

        with allure.step("Проверка, что ответ содержит статус 200 и токен доступа"):
            assert response.status_code == 200, "Ожидался статус 200"
            token = response.json().get("accessToken")
            assert token is not None, "Отсутствует токен доступа"
            allure.attach(token, name="Токен доступа", attachment_type=allure.attachment_type.TEXT)

    @allure.story("Вход с некорректными учетными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Вход с неверными учетными данными должен вернуть 401")
    def test_login_wrong_credentials(self, client):
        wrong_user = {"email": "wrong@yandex.ru", "password": "654321"}

        with allure.step("Отправка запроса на вход с неверными учетными данными"):
            response = client.login_user(wrong_user)

        with allure.step("Проверка, что возвращён статус 401 и корректное сообщение об ошибке"):
            assert response.status_code == 401, "Ожидался статус 401"
            message = response.json().get("message")
            assert message == "email or password are incorrect", f"Неожиданное сообщение: {message}"
