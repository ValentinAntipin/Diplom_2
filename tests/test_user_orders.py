import pytest
import allure
from utils.api_client import ApiClient
from data.user_data import generate_user

client = ApiClient()
VALID_INGREDIENTS = ["61c0c5a71d1f82001bdaaa6d"]

@pytest.fixture
def auth_token():
    user = generate_user()
    client.create_user(user)
    token = client.login_user(user).json()["accessToken"].split("Bearer ")[-1]
    # Создаем заказ, чтобы у пользователя был хотя бы один заказ
    client.create_order(VALID_INGREDIENTS, token)
    return token

@allure.epic("Заказы пользователя")
@allure.feature("Получение заказов")
class TestUserOrders:

    @allure.story("Получение заказов авторизованного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Авторизованный пользователь должен получать список заказов")
    def test_get_orders_authorized_user(self, auth_token):
        with allure.step("Отправка запроса на получение заказов с авторизацией"):
            response = client.get_user_orders(auth_token)

        with allure.step("Проверка, что ответ имеет статус 200 и содержит список заказов"):
            assert response.status_code == 200, f"Ожидался статус 200, но получили {response.status_code}"
            orders = response.json().get("orders")
            assert orders is not None, "Список заказов не должен быть пустым"
            allure.attach(str(orders), name="Список заказов", attachment_type=allure.attachment_type.JSON)

    @allure.story("Получение заказов неавторизованного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Неавторизованный пользователь должен получить 401")
    def test_get_orders_unauthorized_user(self):
        with allure.step("Отправка запроса на получение заказов без авторизации"):
            response = client.get_user_orders("")

        with allure.step("Проверка, что получен статус 401 и корректное сообщение об ошибке"):
            assert response.status_code == 401, f"Ожидался статус 401, но получили {response.status_code}"
            message = response.json().get("message")
            assert message == "You should be authorised", f"Неожиданное сообщение: {message}"
