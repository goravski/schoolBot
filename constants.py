# Базовый URL
url_base = "https://schools.by"
# URL для отправки POST запроса с данными авторизации
url_login = "https://schools.by/login"

# "User-Agent" определяем в глобальных переменных и указываем в запросах,
# так как программа в каждом запросе устанавливает "User-Agent" по умолчанию = Python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}


bot_token = "6349299772:AAFT1JiUtOLsShA1TQoOj4WLg8yVdEfW7SQ"
bot_name = "SchoolByDairyBot"
