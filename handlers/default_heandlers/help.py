from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS, ALLOWED_USERS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, 'Доступные команды:\n{}'.format("\n".join(text)))
