from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS, ALLOWED_USERS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    if message.from_user.id in ALLOWED_USERS:
        text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
        bot.reply_to(message, 'Доступные команды:\n{}'.format("\n".join(text)))
    else:
        bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.full_name}! "
                                               f"Я - телеграм бот. "
                                               f"Вам доступны следующие команды:\n"
                                               f"{'\n'.join(["/send_documents"])}")