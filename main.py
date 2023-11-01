import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6414739247:AAGmHdUPE6HwJYtmz_g5wNPScGEugzOf3Lk",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Регистрация "
text_button_1 = "А что это такое? "
text_button_2 = "Адрес мероприятия "
text_button_3 = "Дата проведения "

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        "*Привет! С Наступающим! ☃*"
        "'Выбирай', что хотел бы узнать ",
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, "Супер! *Как тебя зовут*? ")
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, "Очень приятно! 🤝 'С кем-нибудь придёшь?)")
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)



@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, "Окей! В любом случае, мы будем ждать именно *'тебя!'*"
                                      "Спасибо за регистрацию! "
                                      "А также подписывайся на наш [телеграм-канал] (t.me/ChristmasEve23), чтобы быть в курсе всех новостей! ❗",
                     reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "*Это - самое легендарное событие зимы 2023❄*"
                                      "Небольшая команда инициаторов-подростков Коломны решили организовать одно мероприятие в честь *Рождества Христова! *"
                                      "'На нём будут':"
                                      "🥇 Разнообразные игры;"
                                      " Сладкие напитки и вкусная еда;"
                                      "🤝 Очень много общения и новые знакомства;"
                                      " Интересная тема для обсуждения;"
                                      " И не только!"
                                      "*Приходи обязательно, будет очень весело! ‍*", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "'ул. Боинская, д.2 '", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Ждём тебя *06.01.2023* в *15:00*! ", reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()