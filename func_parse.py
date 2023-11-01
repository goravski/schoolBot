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


def get_pearent_page(session) -> str:
    init_token(session=session)
    """Отправляем POST запрос данными авторизации"""
    response = session.post(constants.url_login, data=constants.data)
    write_response_to_file(resp=response, filename="post")
    log.info(f"Post request login code {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    user_1 = soup.findAll(class_="user_type_1")
    href = "Null"
    for i in user_1:
        if "schools" in i["href"] and not "887325" in i["href"]:
            href = i["href"] + "/dnevnik/quarter/80"
            log.info(f"Got reference: {href}")
    # session.headers.update({"Referer": href})
    resp_result = session.get(href, headers=constants.headers)
    write_response_to_file(resp=resp_result, filename="result")
    print(resp_result.status_code)
    return href
