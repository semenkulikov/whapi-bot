from telebot.handler_backends import State, StatesGroup


class GetDocuments(StatesGroup):
    get_invoice = State()
    get_act = State()
