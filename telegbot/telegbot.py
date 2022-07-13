import telebot
from config import keys, TOKEN
from extensions import APIExeption, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


# Для старта работы предусмотрена кнопка "старт"
@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    user_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    text = """Чтобы начать работу, введите команду боту в следующем формате: 
<имя валюты> \ <в какую валюту перевести> \ <количество переводимой валюты>, например:
'рубль евро 100'
Чтобы посмотреть список всех доступных валют, кликните /values"""
    bot.reply_to(message, text, reply_markup=user_markup)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIExeption("Неверное количество параметров, их должно быть 3!")

        quote, base, amount = values

        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} равна {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling()