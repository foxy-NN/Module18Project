import telebot
from config import values, TOKEN
from Extensions import APIException, CurrencyConverter

mybot = telebot.TeleBot(TOKEN)

@mybot.message_handler(commands=['start'])
def handle_start(mess:telebot.types.Message):
    mybot.send_message(mess.chat.id, f"Привет, {mess.chat.first_name} \n я бот-конвертер валют")
    handle_help(mess)

@mybot.message_handler(commands=['help'])
def handle_help(mess:telebot.types.Message):
    message_text = "Введите /values для просмотра списка доступных валют \n \
Для обмена используйте следующий формат: \n <количество переводимой валюты> <название валюты> \
<в какую валюту перевести>.\n Данные разделяйте пробелом"
    mybot.send_message(mess.chat.id, message_text)
@mybot.message_handler(commands=['values'])
def handle_values (mess:telebot.types.Message):
    text = "Доступные валюты"
    for key in values.keys() :
        text="\n".join((text, key,))
    mybot.reply_to(mess,text)

@mybot.message_handler(content_types=['text'])
def exchange(mess:telebot.types.Message):
    try:
        inp_values = mess.text.split(' ')
        if len(inp_values) != 3:
            raise APIException("Неверное количество параметров")
        amount, quote, base = inp_values
        total = CurrencyConverter.get_price(amount, quote, base)
    except APIException as e:
        mybot.reply_to(mess, f'Ошибка запроса\n{e}')
    except Exception as e:
        mybot.reply_to(mess, f'Не удалось обработать команду\n{e}')
    else:
        text = (f"Цена {amount} {values[quote]} = {total} {values[base]}")
        mybot.send_message(mess.chat.id, text)

mybot.polling(none_stop=True, interval=0)