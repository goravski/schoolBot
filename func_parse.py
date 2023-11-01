import requests
from bs4 import BeautifulSoup
import constants
import logging as log


def write_response_to_file(resp, filename):
    with open(f"{filename}.html", "w", encoding="utf-8") as file:
        file.write(resp.text)


def init_token(session):
    """Отправляем GET запрос на страницу авторизации, чтобы получить CSRF-токен"""
    response = session.get(constants.url_login)

    # Указываем Referer. Если не указать, приводит к ошибкам.
    session.headers.update({"Referer": constants.url_base})
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    # Определить параметр CSRF-токен формы для отправки POST запроса
    constants.data["csrfmiddlewaretoken"] = csrf_token
    log.info(f"Token inited: {csrf_token}")


def get_dairy_page(session):
    """Отправляем POST запрос данными авторизации и получаем дневник текущей недели"""
    init_token(session=session)
    # Отправляем запрос на авторизацию
    response = session.post(constants.url_login, data=constants.data)
    log.info(f"Post request login code {response.status_code}")

    # Отправляем запрос на данные дневника текущей недели
    resp_result = session.get(
        parse_for_get_current_dairy_href(response=response), headers=constants.headers
    )
    log.info(f"request dairy page status {resp_result.status_code}")
    return resp_result


def parse_for_get_current_dairy_href(response):
    """Парсим ответ после авторизации для получения ссылки на дневник"""
    soup = BeautifulSoup(response.text, "html.parser")
    user_1 = soup.findAll(class_="user_type_1")
    href = ""
    for i in user_1:
        if "schools" in i["href"] and not "887325" in i["href"]:
            href = i["href"] + "/dnevnik/quarter/80"
            log.info(f"Got reference: {href}")
    return href
