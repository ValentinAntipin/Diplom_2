import allure
from data.user_data import generate_user
from data.response_messages import EMAIL_ALREADY_EXISTS, MISSING_FIELDS_ERROR


@allure.epic("Управление пользователями")
@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.story("Создание уникального пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self, client):
        user = generate_user()

        with allure.step("Отправка запроса на создание нового уникального пользователя"):
            response = client.create_user(user)
            response_data = response.json()

        with allure.step("Проверка, что получен статус 200 и пользователь создан успешно"):
            assert response.status_code == 200
            assert response_data.get("success") is True

        with allure.step("Логин и удаление созданного пользователя"):
            login_response = client.login_user(user)
            access_token = login_response.json().get("accessToken", "").replace("Bearer ", "")
            delete_response = client.delete_user(access_token)
            assert delete_response.status_code == 202

    @allure.story("Создание уже существующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Попытка создать уже существующего пользователя должна вернуть 403")
    def test_create_existing_user(self, client):
        user = generate_user()

        with allure.step("Создание пользователя (первый запрос)"):
            response1 = client.create_user(user)
            assert response1.status_code == 200

        with allure.step("Повторная попытка создать того же пользователя"):
            response2 = client.create_user(user)

        with allure.step("Проверка, что получен статус 403 и соответствующее сообщение об ошибке"):
            assert response2.status_code == 403
            message = response2.json().get("message")
            assert EMAIL_ALREADY_EXISTS in message

        with allure.step("Удаление пользователя после теста"):
            login_response = client.login_user(user)
            access_token = login_response.json().get("accessToken", "").replace("Bearer ", "")
            delete_response = client.delete_user(access_token)
            assert delete_response.status_code == 202

    @allure.story("Создание пользователя с отсутствующим обязательным полем")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Создание пользователя без email должно вернуть 403")
    def test_create_user_missing_field(self, client):
        user = generate_user()
        user.pop("email", None)

        with allure.step("Отправка запроса на создание пользователя без email"):
            response = client.create_user(user)

        with allure.step("Проверка, что получен статус 403 и сообщение об отсутствии обязательных полей"):
            assert response.status_code == 403
            message = response.json().get("message")
            assert MISSING_FIELDS_ERROR in message
