# from telebot.types import Message
#
# from loader import bot
# from states.states import UrlState, GetSettingsState


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

