import pytest
import allure
from utils.api_client import ApiClient
from data.user_data import generate_user

VALID_INGREDIENTS = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa75"]
INVALID_INGREDIENTS = ["invalid_hash"]


@pytest.fixture(scope="session")
def client():
    return ApiClient()


@pytest.fixture
def auth_token(client):
    user = generate_user()

    with allure.step("Создание пользователя"):
        response = client.create_user(user)
        if response.status_code != 200:
            raise RuntimeError(f"Не удалось создать пользователя: {response.status_code}")

    with allure.step("Авторизация пользователя"):
        login = client.login_user(user)
        if login.status_code != 200:
            raise RuntimeError(f"Не удалось авторизовать пользователя: {login.status_code}")

        token = login.json()["accessToken"].split("Bearer ")[-1]

    yield token

    with allure.step("Удаление пользователя после теста"):
        delete = client.delete_user(token)
        if delete.status_code not in [200, 202]:
            raise RuntimeError(f"Ошибка при удалении пользователя: {delete.status_code}")


@pytest.fixture
def auth_token_and_user(client):
    user = generate_user()

    with allure.step("Создание пользователя"):
        create_response = client.create_user(user)
        if create_response.status_code != 200:
            raise RuntimeError(f"Не удалось создать пользователя: {create_response.status_code}")

    with allure.step("Авторизация пользователя"):
        login_response = client.login_user(user)
        if login_response.status_code != 200:
            raise RuntimeError(f"Не удалось авторизовать пользователя: {login_response.status_code}")

        token = login_response.json()["accessToken"].split("Bearer ")[-1]

    yield token, user

    with allure.step("Удаление пользователя после теста"):
        delete_response = client.delete_user(token)
        if delete_response.status_code not in [200, 202]:
            raise RuntimeError(f"Ошибка при удалении пользователя: {delete_response.status_code}")


@pytest.fixture
def registered_user(client):
    user = generate_user()

    with allure.step("Регистрация пользователя"):
        create_response = client.create_user(user)
        if create_response.status_code != 200:
            raise RuntimeError(f"Ошибка при создании пользователя: {create_response.status_code}")

    yield user, create_response

    with allure.step("Удаление зарегистрированного пользователя"):
        login_response = client.login_user(user)
        if login_response.status_code == 200:
            token = login_response.json()["accessToken"].split("Bearer ")[-1]
            delete_response = client.delete_user(token)
            if delete_response.status_code not in [200, 202]:
                raise RuntimeError(f"Ошибка при удалении пользователя: {delete_response.status_code}")



@pytest.fixture
def auth_token_with_order(client, registered_user):
    user_data, _ = registered_user

    # Логинимся
    login_resp = client.login_user(user_data)
    token = login_resp.json().get("accessToken", "").replace("Bearer ", "")

    # Создаем заказ для этого пользователя (пример)
    client.create_order(VALID_INGREDIENTS, token)

    # Возвращаем токен
    return token