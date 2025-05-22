import requests
import allure
from data.constants import BASE_URL

class ApiClient:
    def __init__(self):
        self.session = requests.Session()

    @allure.step("Создание пользователя: {user_data}")
    def create_user(self, user_data):
        return self.session.post(f"{BASE_URL}/auth/register", json=user_data)

    @allure.step("Логин пользователя: {user_data}")
    def login_user(self, user_data):
        return self.session.post(f"{BASE_URL}/auth/login", json=user_data)

    @allure.step("Обновление данных пользователя с токеном: {access_token}")
    def update_user(self, access_token, new_data):
        headers = {"Authorization": f"Bearer {access_token}"}
        return self.session.patch(f"{BASE_URL}/auth/user", headers=headers, json=new_data)

    @allure.step("Создание заказа: {ingredients}, токен: {token}")
    def create_order(self, ingredients, token=None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self.session.post(f"{BASE_URL}/orders", headers=headers, json={"ingredients": ingredients})

    @allure.step("Получение заказов пользователя с токеном: {token}")
    def get_user_orders(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.get(f"{BASE_URL}/orders", headers=headers)