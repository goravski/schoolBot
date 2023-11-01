# Базовый URL
url_base = "https://schools.by"
# URL для отправки POST запроса с данными авторизации
url_login = "https://schools.by/login"

# "User-Agent" определяем в глобальных переменных и указываем в запросах,
# так как программа в каждом запросе устанавливает "User-Agent" по умолчанию = Python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}


# Логин и пароль для авторизации
# login = input("Login:")
# password = input("Введите пароль:")
login = "goravski"
password = "19672731"

data = {
    "username": login,
    "password": password,
    "csrfmiddlewaretoken": "",
    "|123": "|123",
}
