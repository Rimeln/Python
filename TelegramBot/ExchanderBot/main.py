import telebot
from telebot import types
from currency_converter import CurrencyConverter


bot = telebot.TeleBot('API')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Добро пожаловать. Введите сумму')
    bot.register_next_step_handler(message, summa)
def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите число')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        button2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        button3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        button4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, 'Выберите валюту для обмена', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper.split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res,2)}. Можете заново ввести сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слэш')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново ввести сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Введите значение заново')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)