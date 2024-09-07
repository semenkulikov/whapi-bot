from telebot.types import Message
import os
from loader import bot, app_logger, greenAPI
from states.states import GetDocuments, AdminPanel
from config_data.config import (ALLOWED_USERS,
                                STATIC_PATH,
                                API_URL,
                                MEDIA_URL,
                                API_TOKEN_INSTANCE,
                                ID_INSTANCE,
                                ADMIN_ID_WHATSAPP)
from database.models import User
from keyboards.inline.accounts import users_markup
from utils.utils import send_document_to_whatsapp, send_message_to_whatsapp


# @bot.message_handler(state=UrlState.get_url)
# def get_url(message: Message) -> None:
#     """ Хендлер для получения ссылки """
#
#     url = message.text
#     print(url)
#     if not urlparse(url).scheme:
#         bot.send_message(message.from_user.id, "Необходимо ввести корректную ссылку.")
#         return
#     # Здесь сохранение ссылки в бд и рассылка сообщений. Вызывается функция для запросов к апи.
#     bot.send_message(message.from_user.id, "Ссылка сохранена успешно. Началась рассылка сообщений...")
#     bot.set_state(message.from_user.id, None)
#     send_messages_drom(url_path=url, id_user=message.from_user.id)

#
# @bot.callback_query_handler(func=None, state=GetSettingsState.get_settings)
# def interval_or_time(call):
#     if call.data == "interval":
#         bot.send_message(call.message.chat.id, 'Хорошо, напишите промежуток интервала вида min - min (5 - 15).')
#         bot.set_state(call.message.chat.id, GetSettingsState.interval)
#     elif call.data == "time":
#         bot.send_message(call.message.chat.id, "Напишите время рассылки в формате: h:m - h:m (12:00 - 20:00)")
#         bot.set_state(call.message.chat.id, GetSettingsState.time)
#
#     try:
#         account_obj = Account.get(Account.login == login)
#         account_obj.password = password
#         account_obj.save()
#     except Exception:
#         Account.create(
#             login=login,
#             password=password
#         )
#
#     bot.send_message(message.from_user.id, f"Отлично! Текущий пароль: {password}."
#                                            f"\nНовый аккаунт внесен в базу данных.\n"
#                                            f"Если хотите, можно привязать прокси для этого аккаунта.\n"
#                                            f"Вида: http(s)://username:password@proxyurl:proxyport\n"
#                                            f"Http или https пишите исходя из прокси.\n"
#                                            f"Для пропуска введите -.")
#
#     bot.set_state(message.from_user.id, AccountState.get_proxy)


@bot.message_handler(commands=["send_documents"])
def send_document_message(message: Message):
    """ Функция для приема документов от пользователя """
    if message.from_user.id not in ALLOWED_USERS:
        if User.get_or_none(user_id=message.from_user.id) is None:
            User.create(user_id=message.from_user.id,
                        full_name=message.from_user.full_name,
                        username=message.from_user.username,
                        is_premium=message.from_user.is_premium)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["path"] = os.path.normpath(os.path.join(STATIC_PATH,
                                                         f"{message.from_user.id}"))
            os.makedirs(data["path"], exist_ok=True)
        bot.send_message(message.from_user.id, "Принято! Отправьте мне счет. "
                                               "\n(Не забудьте убрать галочку Сжать изображение)")
        bot.set_state(message.from_user.id, GetDocuments.get_invoice)
    else:
        bot.send_message(message.from_user.id, "Вам недоступна эта команда (")


@bot.message_handler(state=GetDocuments.get_invoice, content_types=["document"])
def get_invoice(message: Message):
    """ Функция для приёма счёта """
    with (bot.retrieve_data(message.from_user.id, message.chat.id) as data):
        path = data.get("path") if data.get("path") is not None else \
            os.path.normpath(os.path.join(STATIC_PATH, f"{message.from_user.id}"))
        data["file_name_invoice"] = message.document.file_name

    # Скачивание файла
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    invoice_path = os.path.normpath(os.path.join(path, message.document.file_name))
    with open(invoice_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Сохранение пути в базу данных
    user_obj = User.get(User.user_id == message.from_user.id)
    user_obj.path_to_invoice = invoice_path
    user_obj.save()

    # Отправка следующего состояния
    bot.send_message(message.from_user.id, f"Принято счет {message.document.file_name}.")
    bot.send_message(message.from_user.id, "Теперь отправьте акт")
    app_logger.info(f"Новый счет от {message.from_user.full_name}: {message.document.file_name}")
    bot.set_state(message.from_user.id, GetDocuments.get_act)


@bot.message_handler(state=GetDocuments.get_act, content_types=["document"])
def get_act(message: Message):
    """ Функция для приёма акта """
    with (bot.retrieve_data(message.from_user.id, message.from_user.id) as data):
        path = data.get("path") if data.get("path") is not None else \
            os.path.normpath(os.path.join(STATIC_PATH, f"{message.from_user.id}"))
        file_name_invoice = data.get("file_name_invoice") if data.get("file_name_invoice") is not None else "Счет.pdf"
    # Скачивание файла
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    act_path = os.path.normpath(os.path.join(path, message.document.file_name))
    with open(act_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Сохранение пути в базу данных
    user_obj: User = User.get(User.user_id == message.from_user.id)
    user_obj.path_to_act = act_path
    user_obj.payment_status = True
    user_obj.save()

    # Отправка следующего состояния
    bot.send_message(message.from_user.id, f"Принято акт {message.document.file_name}. Вы успешно отправили документы!")
    app_logger.info(f"Новый акт от {message.from_user.full_name}: {message.document.file_name}")

    # Отправка документов в WhatsApp
    send_message_to_whatsapp(greenAPI, ADMIN_ID_WHATSAPP, f"Внимание! Поступили документы от {user_obj.full_name}")
    app_logger.info("Отправлено сообщение бухгалтеру")
    send_document_to_whatsapp(greenAPI, ADMIN_ID_WHATSAPP, user_obj.path_to_invoice,
                              file_name_invoice, "Счёт")
    app_logger.info(f"Отправлен счет от {user_obj.full_name}")
    send_document_to_whatsapp(greenAPI, ADMIN_ID_WHATSAPP, user_obj.path_to_act,
                              message.document.file_name, "Акт")
    app_logger.info(f"Отправлен акт от {user_obj.full_name}")
    bot.set_state(message.from_user.id, None)


@bot.message_handler(commands=["admin_panel"])
def admin_panel(message: Message):
    if message.from_user.id in ALLOWED_USERS:
        bot.send_message(message.from_user.id, "Админ панель")
        bot.send_message(message.from_user.id, "Все пользователи базы данных:", reply_markup=users_markup())
        bot.set_state(message.from_user.id, AdminPanel.get_users)
    else:
        bot.send_message(message.from_user.id, "У вас недостаточно прав")


@bot.callback_query_handler(func=None, state=AdminPanel.get_users)
def get_user(call):
    if call.data == "Exit":
        bot.send_message(call.message.chat.id, "Вы успешно вышли из админ панели.")
        bot.set_state(call.message.chat.id, None)
    else:
        user_obj: User = User.get_by_id(call.data)
        is_invoice = "Нет" if user_obj.path_to_invoice == "" else "Да"
        is_act = "Нет" if user_obj.path_to_act == "" else "Да"
        bot.send_message(call.message.chat.id, f"Имя: {user_obj.full_name}\n"
                                               f"Телеграм: @{user_obj.username}\n"
                                               f"Статус платежа: {user_obj.payment_status}\n"
                                               f"Отправил счет: {is_invoice}\n"
                                               f"Отправил акт: {is_act}")
