from extentions import ConvertionException, CurrencyConverter
import telebot

from config import TOKEN, keys, payload, headers

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы перевести валюту введите данные в формате:\n<Название валюты в которую хотите перевести>" \
           "\ <Название валюты за которую покупаете>\
            <Какое количество перевести>\nУвидеть список доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        task_values = message.text.split(" ")
        if len(task_values) != 3:
            raise ConvertionException("Неверное количество параметров.")

        quote, base, amount = task_values
        total = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        answer = f'Результат перевода {amount} {base} в {quote} : {total}'
        bot.send_message(message.chat.id, answer)


bot.polling()
