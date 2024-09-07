# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#
# from database.models import Account, Proxy
#
#
# def account_markup():
#     """ Inline buttons для выбора аккаунта """
#     accounts_obj = Account.select()
#     actions = InlineKeyboardMarkup(row_width=2)
#
#     for account in accounts_obj:
#         actions.add(InlineKeyboardButton(text=f"{account.login}", callback_data=account.id))
#
#     return actions
