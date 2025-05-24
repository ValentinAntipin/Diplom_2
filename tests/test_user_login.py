import allure
from data.response_messages import INVALID_CREDENTIALS_ERROR


@allure.epic("Аутентификация")
@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.story("Успешный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Успешная авторизация с корректными данными")
    def test_successful_login(self, client, registered_user):
        user, _ = registered_user
        with allure.step("Отправка запроса на логин"):
            response = client.login_user(user)
            response_data = response.json()

            allure.attach(
                str(response_data),
                name="Login Response",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка успешного логина"):
            assert response.status_code == 200
            assert response_data.get("success") is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data

    @allure.story("Неуспешный логин при неправильном пароле")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Попытка логина с неверным паролем должна завершиться ошибкой")
    def test_login_with_wrong_password(self, client, registered_user):
        user, _ = registered_user
        user["password"] = "incorrect_password"

        with allure.step("Попытка логина с неправильным паролем"):
            response = client.login_user(user)
            response_data = response.json()

            allure.attach(
                str(response_data),
                name="Failed Login Response",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка отказа в авторизации"):
            assert response.status_code == 401
            assert response_data.get("message") == INVALID_CREDENTIALS_ERROR
