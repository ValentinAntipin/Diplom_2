import allure
from utils.api_client import ApiClient
from data.user_data import generate_user

client = ApiClient()


@allure.epic("Управление пользователями")
@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.story("Создание уникального пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self):
        user = generate_user()

        with allure.step("Отправка запроса на создание нового уникального пользователя"):
            response = client.create_user(user)

        with allure.step("Проверка, что получен статус 200 и пользователь создан успешно"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
            assert response.json().get("success") is True, "Ожидался успешный ответ, но получено другое значение"

    @allure.story("Создание уже существующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Попытка создать уже существующего пользователя должна вернуть 403")
    def test_create_existing_user(self):
        user = generate_user()

        with allure.step("Создание пользователя (первый запрос)"):
            client.create_user(user)

        with allure.step("Повторная попытка создать того же пользователя"):
            response = client.create_user(user)

        with allure.step("Проверка, что получен статус 403 и соответствующее сообщение об ошибке"):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"
            message = response.json().get("message")
            assert "User already exists" in message, f"Неожиданное сообщение об ошибке: {message}"

    @allure.story("Создание пользователя с отсутствующим обязательным полем")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Создание пользователя без email должно вернуть 403")
    def test_create_user_missing_field(self):
        user = generate_user()
        user.pop("email", None)  # Удаляем email

        with allure.step("Отправка запроса на создание пользователя без email"):
            response = client.create_user(user)

        with allure.step("Проверка, что получен статус 403 и сообщение об отсутствии обязательных полей"):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"
            message = response.json().get("message")
            assert "Email, password and name are required fields" in message, f"Неожиданное сообщение об ошибке: {message}"
