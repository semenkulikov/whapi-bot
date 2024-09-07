from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.send_message(message.from_user.id, f"""
    Здравствуйте, {message.from_user.full_name}! Я - телеграм бот.
Чтобы узнать все мои команды, введите /help
    """)
