import telebot  # Вызов библиотеки telebot
from config import keys, TOKEN  # Вызов валют и токена из файла config
from extensions import APIException, CurrencyConverter  # Вызов классов из файла extensions


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help']) # Обработчик - выдает правила ввода информации
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты, цену которой Вы хотите узнать> \
<имя валюты, в которой Вы хотите узнать цену первой валюты> \
<количество первой валюты> \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values']) # Обработчик - выдает информацию о доступныл валютах
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ]) # Обработчик - конвертирует валюты
def get_price(message: telebot.types.Message):
    values = message.text.split(' ')  # Разделение текста сообщения
    try:
        if len(values) > 3:
            raise APIException('Слишком много параметров. /help')

        if len(values) < 3:
            raise APIException('Слишком мало параметров. /help')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
