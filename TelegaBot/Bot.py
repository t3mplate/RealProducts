import threading

import telebot
from telebot import types
from AI.test import Operations

bot = telebot.TeleBot('5932020939:AAFC56lTYXkvbWdARlxKHlvP4fqlHn_-AoQ')

product_prices = {}
selected_stores = {}
selected_plans = {}
vegan_products = {
    'Морковь': 10,
    'Брокколи': 15,
    'Овсянка': 20,
    'Авокадо': 25,
    'Тофу': 30
}
regular_products = {
    'Курица': 50,
    'Рис': 40,
    'Гречка': 35,
    'Молоко': 30,
    'Яйца': 25
}

op = Operations()

@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Рацион питания')
    button2 = types.KeyboardButton('Цена')
    button3 = types.KeyboardButton('Магазины')
    button4 = types.KeyboardButton('План')
    button5 = types.KeyboardButton('Хочу кушать')
    markup.add(button1, button2, button3, button4, button5)
    mess = f'Привет, <b>{message.from_user.first_name}</b>!\nЯ бот EcoProducts'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, 'Напиши <strong>/info</strong> чтобы узнать больше обо мне ', parse_mode='html')


@bot.message_handler(commands=['info', 'Info', 'INFO'])
def info(message):
    bot.send_message(message.chat.id, '''Я умею подбирать продукты под ваше финансовое состояние''', parse_mode='html')


# обработка выбранного продукта после того как чел нажимает кнопку Цена
def process_price_input(message):
    product_name = message.text
    chat_id = message.chat.id
    product_prices[chat_id] = product_name
    bot.reply_to(message, f"Вы выбрали продукт: {product_name}")
    bot.send_message(message.chat.id, op.getPrice(product_name))



# обработка выбранного магазина после того как чел нажимает кнопку Магазины
def process_store_input(message):
    store_name = message.text
    chat_id = message.chat.id
    selected_stores[chat_id] = store_name
    bot.reply_to(message, f"Вы выбрали магазин: {store_name}")
    bot.send_message(message.chat.id, op.setStore(store_name))



# обработка выбранного плана после того как чел нажимает кнопку План
def process_plan_input(message):
    plan_duration = message.text
    chat_id = message.chat.id
    selected_plans[chat_id] = plan_duration
    bot.reply_to(message, f"Вы выбрали продолжительность плана: {plan_duration}")
    bot.send_message(message.chat.id, op.getSchedule(plan_duration))


@bot.message_handler(func=lambda message: message.text == 'Рацион питания')
def handle_ration(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Веганский')
    button2 = types.KeyboardButton('Обычный')
    back_button = types.KeyboardButton('Назад')
    markup.add(button1, button2, back_button)
    bot.reply_to(message, "Выберите рацион:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Цена')
def handle_price(message):
    bot.reply_to(message, "Введите название продукта цену которого вы хотите узнать:")
    bot.register_next_step_handler(message, process_price_input)


@bot.message_handler(func=lambda message: message.text == 'Магазины')
def handle_stores(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for el in op.store.keys():
        markup.add(types.KeyboardButton(el))
    back_button = types.KeyboardButton('Назад')
    markup.add( back_button)
    bot.reply_to(message, "Выберите название ближайшего к вам магазина:", reply_markup=markup)
    bot.register_next_step_handler(message, process_store_input)


@bot.message_handler(func=lambda message: message.text == 'План')
def handle_plan(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('1 месяц')
    button2 = types.KeyboardButton('Полгода')
    button3 = types.KeyboardButton('Год')
    back_button = types.KeyboardButton('Назад')
    markup.add(button1, button2, button3, back_button)
    bot.reply_to(message, "Выберите продолжительность плана или введите свою:", reply_markup=markup)
    bot.register_next_step_handler(message, process_plan_input)


@bot.message_handler(func=lambda message: message.text == 'Хочу кушать')
def handle_hungry(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Веган')
    button2 = types.KeyboardButton('Любой')
    back_button = types.KeyboardButton('Назад')
    markup.add(button1, button2, back_button)
    bot.reply_to(message, "Какой продукт вы хотите:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Веган')
def handle_regular_ration(message):
    bot.reply_to(message, f"Веган продукт:")
    bot.send_message(message.chat.id, op.getRandomProduct(True))

@bot.message_handler(func=lambda message: message.text == 'Любой')
def handle_regular_ration(message):
    bot.reply_to(message, f"Обычный продукт:")
    bot.send_message(message.chat.id, op.getRandomProduct())
@bot.message_handler(func=lambda message: message.text == 'Веганский')
def handle_vegan_ration(message):
    bot.reply_to(message, "Продукты веганского рациона:")

    def get_diet_and_send_message():
        diet = op.getDiet(True)
        bot.send_message(message.chat.id, diet)

    threading.Thread(target=get_diet_and_send_message).start()
@bot.message_handler(func=lambda message: message.text == 'Обычный')
def handle_regular_ration(message):
    bot.reply_to(message, f"Продукты обычного рациона:")
    bot.send_message(message.chat.id, op.getDiet())



@bot.message_handler(func=lambda message: message.text == 'Назад')
def handle_back(message):
    start(message)

# Handle all other messages.
@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
    'text', 'location', 'contact', 'sticker'])
def default_command(message):
    bot.send_message(message.chat.id, "Такой команды не существует")
    start(message)

bot.polling(none_stop=True)
