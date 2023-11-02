import telebot
import constants
import logging as log
import schoolsAuth

log.basicConfig(
    level=log.INFO,
    filename="schools_logs",
    filemode="w",
    format="%(asctime)s, %(levelname)s, %(message)s",
)

bot = telebot.TeleBot(constants.bot_token)
user = schoolsAuth.UserAthenticationData()


@bot.message_handler(commands=["start"])
def start_message(message):
    msg = bot.reply_to(message, "Введите логин:")
    log.info(f"Request login of {message.from_user.username}")
    bot.register_next_step_handler(msg, authantication_login)


def authantication_login(message):
    try:
        user.data["username"] = message.text
        msg = bot.reply_to(message, "Введите пароль:")
        log.info(f"Request password {message.from_user.username}")
        bot.register_next_step_handler(msg, authantication_password)
    except Exception as e:
        bot.reply_to(message, f"Exception in authantication_login {e.with_traceback}")


def authantication_password(message):
    try:
        user.data["password"] = message.text
        bot.send_message(
            message.chat.id, f"{user.data['username'] }, ждите ответа от сервера..."
        )
        log.info(f"Login and password saved {message.from_user.username}")
    except Exception as e:
        bot.reply_to(
            message, f"Exception in authantication_password {e.with_traceback}"
        )


if __name__ == "__main__":
    bot.infinity_polling(timeout=120)
