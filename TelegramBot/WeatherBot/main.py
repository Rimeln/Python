import telebot
import requests
import json

bot = telebot.TeleBot('ApiBot')
API = '1713a93ad24bc8dc7878105a3ea0e60a'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! Чтобы узнать погоду, введите название города')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city_name = message.text.strip().lower()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}&units=metric')
    if result.status_code == 200:
        weather = json.loads(result.text)
        bot.reply_to(message, f'Сейчас погода в этом городе: {weather["main"]["temp"]}')
    else:
        bot.reply_to(message, "Такого города не существует")

bot.polling(none_stop=True)