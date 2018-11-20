import Variables as var
import telebot
import requests
import datetime, time
import logging
import re


bot = telebot.TeleBot(var.telegram_token, threaded=False)


@bot.message_handler(commands = ['currencynow'])
def cn(message):
    req = requests.get(var.bank_api_url)
    if not req.ok:
        print('ERROR:',req.status_code)
        exit(0)
    mes = req.json()

    for x in range(len(mes)):

        if mes[x]['Cur_Abbreviation'] == 'USD':
            result_message = 'За {} курс {} за 1 {}'.format(str(datetime.date.today()),str(mes[x]["Cur_OfficialRate"]),str(
                mes[x]['Cur_Name']))
            bot.send_message(message.chat.id, result_message)

        if mes[x]['Cur_Abbreviation'] == 'EUR':
            result_message = 'За {} курс {} за 1 {}'.format(str(datetime.date.today()), str(mes[x]["Cur_OfficialRate"]),
                                                            str(
                                                                mes[x]['Cur_Name']))
            bot.send_message(message.chat.id, result_message)

@bot.message_handler(commands = ['currencydate'])
def cn(message):
    msg = bot.send_message(message.chat.id, 'Курс валют за какую дату вас интересует?\nВ формате YYYY-MM-DD')
    bot.register_next_step_handler(msg,reg)


def reg(message):
    if re.match(r'\d{4}-\d{2}-(\d{2})',message.text):
        req = requests.get(var.bank_api_url1 + var.bank_methods['onDate'] + message.text + var.bank_methods['today'])
        if not req.ok:
            print('ERROR:', req.status_code)
            exit(0)
        mes = req.json()
        for x in range(len(mes)):

            if mes[x]['Cur_Abbreviation'] == 'USD':
                result_message = 'За {} курс {} за 1 {}'.format(message.text,
                                                                str(mes[x]["Cur_OfficialRate"]), str( mes[x]['Cur_Name']))
                bot.reply_to(message, result_message)

            if mes[x]['Cur_Abbreviation'] == 'EUR':
                result_message = 'За {} курс {} за 1 {}'.format(message.text,
                                                                str(mes[x]["Cur_OfficialRate"]), str(mes[x]['Cur_Name']))
                bot.reply_to(message, result_message)

    else:
        bot.send_message(message.chat.id, 'Неверный ввод. Введите согласно YYYY-MM-DD')
        cn(message)


@bot.message_handler(commands = ['weathernow'])
def wn(message):
    req = requests.get(var.weather_api_url + var.weather_methods['day'] + "Minsk" + var.weather_token)
    if not req.ok:
        print('ERROR:', req.status_code)
        exit(0)
    mes = req.json()
    place = mes["name"]
    date = time.strftime("%a, %d %b %Y", time.localtime(mes['dt']))
    aver_temp = str(round(mes['main']['temp'] - 273.15))
    pressure = str(round(mes['main']['pressure']))
    sunrise = time.strftime("%H:%M:%S ", time.localtime(mes['sys']['sunrise']))
    sunset = time.strftime("%H:%M:%S ", time.localtime(mes['sys']['sunset']))
    result_message = "\t\t {} \nСегодня: {}\nТемерпатура: {} по цельсию\nДавление: {} pHA\nВосход: {}\nЗакат: {}".format( place, date, aver_temp, pressure, sunrise, sunset)
    bot.send_message(message.chat.id, result_message)


@bot.message_handler(commands=['weatherweek'])
def wk(message):
    req = requests.get(var.weather_api_url + var.weather_methods['week'] + "Minsk" + var.weather_token)
    if not req.ok:
        print('ERROR:', req.status_code)
        exit(0)
    mes = req.json()

    for x in range(mes['cnt']):
        place = mes['city']["name"]
        date = time.strftime("%a, %d %b %Y", time.localtime(mes['list'][x]['dt']))
        dt = mes['list'][x]['dt_txt']
        aver_temp = str(round(mes['list'][x]['main']['temp'] - 273.15))
        pressure = str(round(mes['list'][x]['main']['pressure']))
        result_message = "\t\t {} \nДата: {}\nТемерпатура: {} по цельсию\nДавление: {} pHA\n".format(
            place, date, aver_temp, pressure)

        if x == 0:
            bot.send_message(message.chat.id, result_message)
            continue

        if re.findall(r'\d{2}:\d{2}:\d{2}',dt) == ['15:00:00']:
            bot.send_message(message.chat.id, result_message)
            continue


@bot.message_handler(commands=['lastfive'])
def resmsg(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id,
                     "Отправь мне свой номер телефона или поделись местоположением, жалкий человечишка!",
                     reply_markup=keyboard)
    bot.forward_message(message.chat.id,message.chat.id,message.message_id-5)


if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(True)

        except Exception as e:
            logging.error(e)
            time.sleep(15)