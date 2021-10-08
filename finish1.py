from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot

import sqlite3 as sql

roat = ''
exex = ''

bot = telebot.TeleBot("1916736351:AAGrOdSS81pWv4Luo0sj_KVaK-RUaKjWCOg")


def start_marcup():
    marcup = InlineKeyboardMarkup()
    marcup.row_width = 2
    marcup.add(InlineKeyboardButton("к выбору маршрута", callback_data="/add_start"))
    # marcup.add(InlineKeyboardButton("по идее кнопка назад", callback_data="/back"))
    marcup.add(InlineKeyboardButton("список маршруов", callback_data="/roat"),
               InlineKeyboardButton("список остановок", callback_data="/stop_bus"))

    return marcup


@bot.message_handler(commands=['start', 'main_menu'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!!! '.format(message.from_user) +
        'Это бот который поможет тебе узнать расписание маршруток.\n', reply_markup=start_marcup())


# список кортежей маршрутов
def get_roat_list():
    with sql.connect('Raspisanie_bus_Test1BD.db3') as db:
        curs = db.cursor()
        curs.execute('SELECT * FROM roat')

        return curs.fetchall()


print(1, '=', 'get_roat_list()', get_roat_list())
# список кортежей отсановок


def get_stop_bus_list():
    with sql.connect('Raspisanie_bus_Test1BD.db3') as db:
        curs = db.cursor()
        curs.execute('SELECT roat_number, stop_bus FROM stop_roat')

        return curs.fetchall()


print('2 =get_stop_bus_list()', type(get_stop_bus_list()), get_stop_bus_list())


# def get_roat_dict():
#     stop_bus = {}
#     for i in get_roat_list()[0]:
#         stop_bus[i] = get_roat_list()[1]
#     return stop_bus
#
# print("2.1 = get_stop_bus_dict()", type(get_roat_dict()), get_roat_dict())
#------------------------пытаюсь использовать словарь

# список маршрутов в стр
def roat_list_str():
    roat_list = ""
    for i in get_roat_list():
        roat_list += f'{i[0]} направление: {i[1]}\n'
    return roat_list


print(3, '= roat_list_str()', type(roat_list_str()), '\n', roat_list_str())

# список остановок(номер маршрута) в стр


def stop_bus_str():
    stop_bus_list = ""
    for i in get_stop_bus_list():
        stop_bus_list += f'{i[1]} ({i[0]})\n'
    return stop_bus_list


# print("3.1 = stop_bus_str()", type(stop_bus_str()), "\n", stop_bus_str())


# список номеров направления в списке
def get_roat_names():
    roat_names = []
    for i in get_roat_list():
        roat_names.append((i[0]))
    return roat_names


print(4, '= get_roat_names', type(get_roat_names()), get_roat_names())


# список остановок


def get_stop_bus_names():
    stop_bus = []
    for i in get_stop_bus_list():
        stop_bus.append(i[1])
    return stop_bus


# print("5 = get_stopbus_names", type(get_stop_bus_names()), get_stop_bus_names())


# создадим кнопки

def get_roat_marcup():
    marcup = InlineKeyboardMarkup()
    marcup.row_width = 3 # -----------------------------понять как должно работать
    for g in get_roat_names():
        marcup.add(InlineKeyboardButton(g, callback_data=g))
    return marcup

# кнопки остановок


def get_stop_bus_marcup():
    marcup = InlineKeyboardMarkup()
    for st in get_stop_bus_list():
        marcup.add(InlineKeyboardButton(f'=={st[1]} ({st[0]})', callback_data=st[0]))
    return marcup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global roat
    global exex
    # выводим список маршруток и направлений их
    if call.data == "/roat":
        bot.send_message(call.message.chat.id,
                         f'{roat_list_str()}/main_menu')

    elif call.data == "/stop_bus":
        bot.send_message(
            call.message.chat.id,
            f'{stop_bus_str()}/main_menu'
        )

    # Создаем меню выбора маршруток
    elif call.data == '/add_start':
        roat = ''
        bot.send_message(
            call.message.chat.id,
            f'Выбирите номер маршрута',
            reply_markup=get_roat_marcup()
        )
    elif call.data in get_roat_names():
        roat = call.data
        marcup = InlineKeyboardMarkup()
        marcup.add(InlineKeyboardButton('ДА нах...Погнали!', callback_data="/stop_roat"),
                   InlineKeyboardButton("СТОПЭ!! Ворочай назат!", callback_data="/add_start"))
        bot.send_message(
            call.message.chat.id,
            f'выбрана маршрутка:{roat}',
            reply_markup=marcup
        )

    # Создаем меню выбора остановки
    elif call.data == "/stop_roat":
        exex = ''
        bot.send_message(
            call.message.chat.id,
            f'Выбери остановку :',
            reply_markup=get_stop_bus_marcup()
            )
    # Создаем меню подтверждения добавления остановки
    elif call.data in get_stop_bus_names():
        exex = call.data
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Добавить подход', callback_data='/new_rep'),
                   InlineKeyboardButton('Выбрать другое упражнение', callback_data='/stop_roat'))
        bot.send_message(
            call.message.chat.id,
            f'Название остановки: {exex}',
            reply_markup=markup
        )
    # Выводим информацию по добавлению остановки
    elif call.data == '/new_rep':
        exex = call.data
        bot.send_message(
            call.message.chat.id,
            f'маршрут: {roat}. остановка: {exex}.\nВведите данные подхода в формате: вес кол-во'
        )


print('Bot in work....')

bot.polling(none_stop=True, interval=0)