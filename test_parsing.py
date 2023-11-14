import schoolsAuth
import requests
import func_parse as fp
import logging as log

log.basicConfig(
    level=log.INFO,
    filename="schools_logs",
    filemode="w",
    format="%(asctime)s, %(levelname)s, %(message)s",
)

user = schoolsAuth.UserAthenticationData()

user.data["username"] = "goravski"
user.data["password"] = ""
user.data["|123"] = "|123"


def write_response_to_file(resp, filename):
    with open(f"{filename}.html", "w", encoding="utf-8") as file:
        file.write(resp.text)


def write_dict_to_file(dict, filename):
    with open(f"{filename}.txt", "a", encoding="utf-8") as file:
        for key, values in dict.items():
            file.write(f"{key}\n")
            for value in values:
                file.write(f"{value}\n")


fp.get_dairy_page(user)
