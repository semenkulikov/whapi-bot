from telebot.types import Message
from loader import bot, app_logger
from config_data.config import DEFAULT_COMMANDS, ALLOWED_USERS
from database.models import User, Group


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    if message.chat.type == "private":
        if User.get_or_none(user_id=message.from_user.id) is None:
            User.create(user_id=message.from_user.id,
                        full_name=message.from_user.full_name,
                        username=message.from_user.username,
                        is_premium=message.from_user.is_premium)
        if message.from_user.id in ALLOWED_USERS:
            commands = [f"/{command} - {description}" for command, description in DEFAULT_COMMANDS]
            bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.full_name}! "
                                                   f"Вы в списке администраторов бота. "
                                                   f"Вам доступны следующие команды:\n"
                                                   f"{'\n'.join(commands)}")
        else:
            app_logger.info(f"Внимание! Новый юзер: {message.from_user.full_name} - {message.from_user.id}")
            bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.full_name}! "
                                                   f"Я - телеграм бот. "
                                                   f"Вам доступны следующие команды:\n"
                                                   f"{'\n'.join(["/send_documents"])}")

    else:
        bot.send_message(message.chat.id, "Здравствуйте! Я - телеграм бот, модератор каналов и групп. "
                                          "Чтобы получить больше информации, "
                                          "обратитесь к администратору.")
        if Group.get_or_none(group_id=message.chat.id) is None:
            Group.create(group_id=message.chat.id,
                         title=message.chat.title,
                         description=message.chat.description,
                         bio=message.chat.bio,
                         invite_link=message.chat.invite_link,
                         location=message.chat.location,
                         username=message.chat.username)
        if User.get_or_none(user_id=message.from_user.id) is None:
            User.create(user_id=message.from_user.id,
                        full_name=message.from_user.full_name,
                        username=message.from_user.username,
                        is_premium=message.from_user.is_premium)
