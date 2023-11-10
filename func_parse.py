import requests
from bs4 import BeautifulSoup
import constants
import logging as log


def write_response_to_file(resp, filename):
    with open(f"{filename}.html", "w", encoding="utf-8") as file:
        file.write(resp.text)


def init_token(user):
    """Отправляем GET запрос на страницу авторизации, чтобы получить CSRF-токен"""

    log.info(f"def init_token make request to url: {constants.url_login}")
    session = requests.Session()

    response = session.get(constants.url_login)
    log.info(f"get login response {response.status_code}")
    # Указываем Referer. Если не указать, приводит к ошибкам.
    session.headers.update({"Referer": constants.url_base})
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    # Определить параметр CSRF-токен формы для отправки POST запроса
    user.data["csrfmiddlewaretoken"] = csrf_token
    user.session = session
    log.info(f"Token inited: {csrf_token}")


def get_dairy_page(user):
    """Отправляем POST запрос данными авторизации и получаем дневник текущей недели"""
    init_token(user=user)
    # Отправляем запрос на авторизацию
    response = user.session.post(constants.url_login, data=user.data)
    log.info(f"get_dairy_page() - Authorization status code {response.status_code}")

    # Отправляем запрос на данные для выбора периода
    href_quarter = parse_for_get_dairy_href(response=response)
    resp_quarter = user.session.get(href_quarter, headers=constants.headers)
    log.info(
        f"get_dairy_page() - Request quarter's page status code {resp_quarter.status_code}"
    )

    # Отправляем запрос на данные для текущего дневника
    href_dairy = href_quarter + parse_for_get_current_dairy_href(resp_quarter)
    log.info(f"get_dairy_page() - result dairy href{href_dairy}")
    resp_result = user.session.get(href_dairy, headers=constants.headers)
    log.info(
        f"get_dairy_page() - request current dairy page status code {resp_result.status_code}"
    )
    write_response_to_file(resp_result, "result")
    return resp_result


def parse_for_get_dairy_href(response):
    """Парсим ответ после авторизации для получения ссылки на выбор периода"""
    soup = BeautifulSoup(response.text, "html.parser")
    user_1 = soup.findAll(class_="user_type_1")
    href = ""
    for i in user_1:
        if "schools" in i["href"] and not "887325" in i["href"]:
            href = i["href"] + "/dnevnik"
            log.info(f"parse_for_get_dairy_href - got reference: {href}")
    return href


def parse_for_get_current_dairy_href(response):
    """Парсим ответ после выбора периода для получения ссылки на дневник выбранной недели"""
    soup = BeautifulSoup(response.text, "html.parser")
    resp1 = soup.findAll("a", class_="current")
    href_items = resp1[0].get("src").split("/")
    href_dairy = f"/{href_items[4]}/{href_items[5]}"
    log.info(f"parse_for_get_current_dairy_href - got reference: {href_dairy}")

    return href_dairy
