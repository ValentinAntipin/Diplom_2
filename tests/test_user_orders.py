import allure
from data.response_messages import UNAUTHORIZED_ERROR
import json

@allure.epic("Заказы пользователя")
@allure.feature("Получение заказов")
class TestUserOrders:

    @allure.story("Получение заказов авторизованного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Авторизованный пользователь должен получать список заказов")
    def test_get_orders_authorized_user(self, client, auth_token_with_order):
        with allure.step("Отправка запроса на получение заказов с авторизацией"):
            response = client.get_user_orders(auth_token_with_order)

        with allure.step("Проверка, что ответ имеет статус 200 и содержит список заказов"):
            assert response.status_code == 200, f"Ожидался статус 200, но получили {response.status_code}"
            orders = response.json().get("orders")
            assert orders is not None, "Список заказов не должен быть пустым"
            allure.attach(json.dumps(orders, ensure_ascii=False, indent=2), name="Список заказов", attachment_type=allure.attachment_type.JSON)

    @allure.story("Получение заказов неавторизованного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Неавторизованный пользователь должен получить 401")
    def test_get_orders_unauthorized_user(self, client):
        with allure.step("Отправка запроса на получение заказов без авторизации"):
            response = client.get_user_orders("")

        with allure.step("Проверка, что получен статус 401 и корректное сообщение об ошибке"):
            assert response.status_code == 401, f"Ожидался статус 401, но получили {response.status_code}"
            message = response.json().get("message")
            assert message == UNAUTHORIZED_ERROR, f"Неожиданное сообщение: {message}"
