# whapi-bot
Bot for managing counterparts in Telegram and forwarding messages in WhatsApp

Функционал:
* Этот бот разработан для контроля над платежеспособностью контрагентов.
*  Команда /start запускает бота, далее он требует от пользователя документы (счет и акт)
* Если id юзера входит в админский список, этому пользователю доступна админка.
* В админке можно посмотреть статусы платежей для каждого пользователя.
* После получения документов бот пересылает их в WhatsApp бухгалтеру (id которого тоже должно быть в списке разрешенных)


Стек:
* Python 3.12
* pythonTelegramBotAPI
* whatsapp-api-client-python
* Peewee
* python-dotenv
* requests
* telebot-calendar
* urllib3
