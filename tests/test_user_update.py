import allure
from data.response_messages import UNAUTHORIZED_ERROR


@allure.epic("Управление пользователями")
@allure.feature("Обновление данных пользователя")
class TestUserUpdate:

    @allure.story("Обновление данных авторизованного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Авторизованный пользователь должен иметь возможность обновить свои данные")
    def test_update_user_authorized(self, client, auth_token_and_user):
        token, _ = auth_token_and_user
        new_data = {"name": "Обновлённое имя"}

        with allure.step("Отправка запроса на обновление данных пользователя с токеном"):
            response = client.update_user(token, new_data)

        with allure.step("Проверка, что получен статус 200 и имя пользователя обновлено"):
            assert response.status_code == 200
            updated_name = response.json()["user"]["name"]
            assert updated_name == "Обновлённое имя"
            allure.attach(str(response.json()), name="Обновлённые данные пользователя", attachment_type=allure.attachment_type.JSON)

    @allure.story("Попытка обновления данных без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Неавторизованный пользователь не должен иметь возможность обновлять данные")
    def test_update_user_unauthorized(self, client):
        new_data = {"name": "Взломщик"}

        with allure.step("Отправка запроса на обновление данных без токена авторизации"):
            response = client.update_user("", new_data)

        with allure.step("Проверка, что возвращён статус 401 и сообщение требует авторизации"):
            assert response.status_code == 401
            message = response.json().get("message")
            assert message == UNAUTHORIZED_ERROR
            allure.attach(str(response.json()), name="Ошибка авторизации", attachment_type=allure.attachment_type.JSON)
