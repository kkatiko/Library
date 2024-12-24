from locust import HttpUser, task, between
import random
import string
from bs4 import BeautifulSoup

def generate_random_username(length=15):
    #Генерация случайного имени пользователя.
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_password(length=15):
    #Генерация случайного пароля.
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    csrf_token = None

    def on_start(self):
        # Получаем CSRF-токен при старте пользователя
        response = self.client.get("/register/")
        self.csrf_token = self.extract_csrf_token(response.text)

    def extract_csrf_token(self, html):
        #Извлекает CSRF-токен из HTML-кода.
        soup = BeautifulSoup(html, 'html.parser')
        token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        return token['value'] if token else None

    @task(1)
    def register_user(self):
        #Регистрация нового пользователя.
        username = generate_random_username()
        password = generate_random_password()
        response = self.client.post("/register/", {
            'username': username,
            'password1': password,
            'password2': password,
            'csrfmiddlewaretoken': self.csrf_token  # Включаем CSRF-токен
        })
        if response.status_code == 200:
            print(f"User {username} registered successfully.")
        else:
            print(f"Failed to register user {username}: {response.status_code} - {response.text}")

    @task(2)
    def view_catalog(self):
        #Просмотр каталога книг.
        self.client.get("/catalog/")
