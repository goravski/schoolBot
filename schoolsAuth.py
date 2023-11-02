import requests
from bs4 import BeautifulSoup
import func_parse as fp


class UserAthenticationData:
    # Логин и пароль для авторизации
    login = "goravski"
    password = "19672731"

    data = {
        "username": login,
        "password": password,
        "csrfmiddlewaretoken": "",
        "|123": "|123",
    }
    session = requests.Session()

    # hre = fp.get_dairy_page(session=session)
    # print(f"HREF :{hre}")
