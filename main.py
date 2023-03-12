import telebot
from telebot import types
import db
import mail
from constants import *
from hashlib import md5
from random import randint


db.connect()
bot = telebot.TeleBot(TOKEN)


users_status = {}
users_question = {}
users_secrets = {}
users_trial_emails = {}


def make_buttons(names):
    markup = types.InlineKeyboardMarkup()
    for name in names:
        markup.add(types.InlineKeyboardButton(name, callback_data=md5(name.encode()).hexdigest()))
    return markup


def make_keyboard_buttons(names):
    markup = types.ReplyKeyboardMarkup()
    for name in names:
        markup.add(types.KeyboardButton(name))
    return markup


def question_string(id):
    return list(QUESTIONS.keys())[users_question[id]]


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.send_message(message.from_user.id, WELCOME_MESSAGE,
                     reply_markup=make_keyboard_buttons([RANDOM_GIF_BUTTON_NAME, RECOVER_PASS_BUTTON_NAME]))


def password_recovery(message):
    data = db.get_pass_by_email(message.text)
    if message.from_user.id not in users_status:
        users_status[message.from_user.id] = USER_FIRST_TRY
    if data:
        bot.send_message(message.from_user.id, ANSWER_QUESTIONS)
        users_question[message.from_user.id] = 0
        users_status[message.from_user.id] = USER_FINAL_QUESTION
        users_secrets[message.from_user.id] = (message.text, data)
        bot.send_message(message.from_user.id, question_string(message.from_user.id),
                         reply_markup=make_buttons(list(QUESTIONS.values())[users_question[message.from_user.id]][0]), parse_mode='HTML')
    else:
        if users_status[message.from_user.id] == USER_FIRST_TRY:
            bot.send_message(message.from_user.id, SECOND_TRY_MESSAGE)
            users_status[message.from_user.id] = USER_SECOND_TRY
            users_trial_emails[message.from_user.id] = [message.text]
        else:
            bot.send_message(message.from_user.id, CAN_NOT_FIND)
            users_status[message.from_user.id] = USER_LOGIN
            users_trial_emails[message.from_user.id].append(message.text)


def answer_questions(message):
    if md5(list(QUESTIONS.values())[users_question[message.from_user.id]][1].encode()).hexdigest() == message.data:
        bot.edit_message_reply_markup(message.message.chat.id, message.message.id, None)
        if users_question[message.from_user.id] != len(QUESTIONS) - 1:
            users_question[message.from_user.id] += 1
            users_status[message.from_user.id] = USER_FINAL_QUESTION
            bot.send_message(message.from_user.id,
                             question_string(message.from_user.id),
                             reply_markup=make_buttons(list(QUESTIONS.values())[users_question[message.from_user.id]][0]), parse_mode='HTML')
        else:
            bot.send_message(message.from_user.id, SUCCESS)
            mail.send(users_secrets[message.from_user.id][0], 'Ваш пароль. IChazy',
                      f"""
                      Похоже вы забыли ваш пароль.
                      Ваш пароль: {users_secrets[message.from_user.id][1]}
                      """)
            delete_user(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, QUESTION_FAILURE_MESSAGE)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    answer_questions(call)


def random_gif(message):
    bot.send_video(message.from_user.id, CUTIES[randint(0, len(CUTIES) - 1)],
                     reply_markup=make_keyboard_buttons([RANDOM_GIF_BUTTON_NAME, RECOVER_PASS_BUTTON_NAME]))


def delete_user(user_id):
    users_status.pop(user_id, None)
    users_question.pop(user_id, None)
    users_secrets.pop(user_id, None)
    users_trial_emails.pop(user_id, None)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == RECOVER_PASS_BUTTON_NAME:
        bot.send_message(message.from_user.id, GET_EMAIL_MESSAGE)
    elif message.text == RANDOM_GIF_BUTTON_NAME:
        random_gif(message)
    elif '@' in message.text:
        password_recovery(message)
    elif message.from_user.id in users_status:
        if users_status[message.from_user.id] in [USER_FINAL_QUESTION, USER_FINAL_QUESTION_SECOND_TRY]:
            answer_questions(message)
        elif users_status[message.from_user.id] == USER_LOGIN:
            mail.send(SUPPORT_EMAIL, f'USER: {message.text}', f'EMAILS: {" ".join(users_trial_emails[message.from_user.id])}\n'
                                                              f'USER: {message.text}\n'
                                                              f'Telegram username: {message.from_user.username}')
            bot.send_message(message.from_user.id, GOT_LOGIN)
            delete_user(message.from_user.id)


bot.polling(none_stop=True, interval=0)
