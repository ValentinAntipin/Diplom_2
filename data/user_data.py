import random
import string

def generate_user():
    email = f"user_{random.randint(10000,99999)}@test.ru"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return {"email": email, "password": password, "name": "Test User"}