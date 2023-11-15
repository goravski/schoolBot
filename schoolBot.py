import telebot
from telebot import types
import constants
import logging as log
import schoolsAuth
import func_parse as fp

log.basicConfig(
    level=log.INFO,
    filename="schools_logs",
    filemode="a",
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
        "Добрый день!\n"
        + "Для получения дневника текущей недели нажмите внизу экрана кнопку <Обновить>"
        + "и введите по запросу логин и пароль для входа на сайт schools.by"
    )
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(content_types="text")
def message_reply(message):
    if message.text == "Обновить":
        msg = bot.reply_to(message, "Введите логин:")
        bot.register_next_step_handler(msg, authantication_login)
        log.info(
            f"message_reply() - Request login of user {message.from_user.username}"
        )


def authantication_login(message):
    try:
        user.data["username"] = message.text
        msg = bot.reply_to(message, "Введите пароль:")
        log.info(
            f"authantication_login() - Request password of user :{message.from_user.username}"
        )
        bot.register_next_step_handler(msg, authantication_password)
    except Exception as e:
        bot.reply_to(message, f"Exception in authantication_login() {e.with_traceback}")
        log.warning(f"Exception in authantication_login() {e}")


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
        text = fp.transform_dict_to_text(dairy)
        log.info(f"authantication_password - text ready")
        bot.send_message(
            message.chat.id,
            text=text,
            parse_mode="Markdown",
        )

        bot.send_message(
            message.chat.id,
            text="_Для получения обновленной информации нажмите кнопку <Обновить>"
            + "или введите текст 'Обновить' и повторно введите логин и пароль_",
            parse_mode="Markdown",
        )
        log.info(f"Sent dairy to chat")
    except Exception as e:
        log.warning(f"Exception in authantication_password. Exception: {e}")
        if e.__cause__ is None:
            bot.reply_to(
                message, f"Ошиблись логином или паролем. \n Нажмите 'Обновить'"
            )
        else:
            bot.reply_to(message, f"Ошибка обработки данных. \n Попробуйте позже")


try:
    bot.infinity_polling(interval=0)
except TimeoutError:
    log.warning(f"Timed out")
except ConnectionError:
    log.warning(f"Disconnected")
