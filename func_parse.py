import requests
from bs4 import BeautifulSoup
import constants
import logging as log
import re


def transform_dict_to_text(dict) -> str:
    text = ""
    for key, values in dict.items():
        text += "".join(f"\n*{key}*\n")
        for value in values:
            str = ""
            str += value[0]
            while len(str) < 40:
                str += " "
            str += f"оценка = _{value[2]}_ \n"
            str += f"        д/з: _{value[1]}_ \n"
            text += str
    return text


def init_token(user):
    """Отправляем GET запрос на страницу авторизации, чтобы получить CSRF-токен"""

    log.info(f"init_token() - make request to url: {constants.url_login}")
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
    log.info(f"init_token () = Token inited: {csrf_token}")


def get_dairy_page(user):
    """Отправляем POST запрос данными авторизации и получаем дневник текущей недели"""
    try:
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
        return parse_get_week_lessons(resp_result)
    except Exception as e:
        log.warning(f"Exception in get_dairy_page () Invalid login or password {e}")


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


def parse_get_week_lessons(response) -> dict:
    try:
        """Разбираем страницу дневника и складываем в словарь,
        где {"день недели, число" : [список предметов[предмет, дом. задание, оценка]]}
        """
        response_text = re.sub(r">\s+<", "><", response.text.replace("\n", ""))
        soup = BeautifulSoup(response_text, "html.parser")
        days = soup.findAll("div", class_="db_day")

        log.info(f"parse_get_week_lessons - got days soup")
        week_dict = {}
        # В словарь по порядку присваиваем значение дня ключю и инициируем список "День"
        for day in days:
            date = get_element_of_day(list(day.find("th", class_="lesson").strings), 0)
            day_list = []

            week_dict[date] = day_list
            log.info(f"parse_get_week_lessons - intited day {date}")
            # В "День" передаем значение предметов
            for lesson in day.findAll("td", class_="lesson"):
                lesson_list = []
                lesson_list.append(
                    get_element_of_day(list(lesson.strings), 0).replace(" ", "")
                )
                day_list.append(lesson_list)

            # В "День" передаем значение заданий на дом
            i = 0
            for task in day.findAll("td", class_="ht"):
                home_task = task.findAll("div", class_="ht-text")
                if home_task:
                    day_list[i].append(home_task[0].getText().strip())
                else:
                    day_list[i].append(" ")
                i += 1
            # В "День" передаем значение оценок
            i = 0
            for mark in day.findAll("div", class_="mark_box"):
                day_list[i].append(get_element_of_day(list(mark.strings), 0))
                i += 1
        log.info(f"parse_get_week_lessons() - send week_dict")
        return week_dict
    except Exception as e:
        log.warning(f"Exception in parse_get_week_lessons (): {e}")


def get_element_of_day(element_list, int) -> str:
    """Проверка списка на пустоту и инициирование пробелом"""
    if element_list:
        return element_list[int]
    else:
        return " "
