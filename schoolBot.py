import telebot
from telebot import types
import constants
import logging as log
import schoolsAuth
import func_parse as fp

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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Обновить")
    markup.add(button)
    text = (
        "Добрый день!\n Для получения дневника текущей недели нажмите кнопку <Обновить>"
        + "и введите по запросу логин и пароль для входа на сайт schools.by"
    )
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(content_types="text")
def message_teply(message):
    if message.text == "Обновить":
        msg = bot.reply_to(message, "Введите логин:")
        log.info(f"Request login of {message.from_user.username}")
        bot.register_next_step_handler(msg, authantication_login)


def authantication_login(message):
    try:
        log.info(f"USER object data: {user.data}")
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
        log.info(
            f"authantication_password - Login and password saved {message.from_user.username}"
        )
        dairy = fp.get_dairy_page(user)
        log.info(f"authantication_password - got dairy")
        text = fp.transform_dict_to_text(dairy)
        log.info(f"authantication_password - got text {text}")
        bot.send_message(message.chat.id, text=text)
        log.info(f"Send day list: {text}")
        bot.send_message(
            message.chat.id,
            text="Для получения обновленной информации нажмите кнопку <Обновить>"
            + "или введите текст 'Обновить' и повторно введите логин и пароль",
        )

    except Exception as e:
        bot.reply_to(message, f"Exception in authantication_password {e}")


bot.infinity_polling(interval=0)
