import telebot
import constants
import logging
import schoolsAuth

logging.basicConfig(
    level=logging.INFO,
    filename="schools_logs",
    filemode="w",
    format="%(asctime)s, %(levelname)s, %(message)s",
)

bot = telebot.TeleBot(constants.bot_token)
user = schoolsAuth.UserAthenticationData()


@bot.message_handler(commands=["start"])
def start_message(message):
    msg = bot.reply_to(message, "Введите логин:")
    bot.register_next_step_handler(msg, authantication_login)


def authantication_login(message):
    user.data["username"] = message.text
    msg = bot.reply_to(message, "Введите пароль:")
    bot.register_next_step_handler(msg, authantication_password)


def authantication_password(message):
    user.data["password"] = message.text
    print(user.data)
    bot.send_message(
        message.chat.id, f"{user.data['username']} Ждите ответа от сервера..."
    )


if __name__ == "__main__":
    bot.infinity_polling()
