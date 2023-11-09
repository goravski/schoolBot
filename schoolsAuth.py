import requests
from bs4 import BeautifulSoup


class UserAthenticationData:
    # Логин и пароль для авторизации
    data = {
        "username": "goravsk",
        "password": "1967273",
        "csrfmiddlewaretoken": "",
        "|123": "|123",
    }

    def __init__(self):
        self.data["username"] = ""
        self.data["password"] = ""
        self.data["csrfmiddlewaretoken"] = ""
        self.data["|123"] = "|123"
