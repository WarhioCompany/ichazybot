import telebot
from telebot import types
import db
from send_mails import *
from hashlib import md5
from random import randint
import threading
import promocodes as promo
from constants import *
import re


def start_thread(func):
    x = threading.Thread(target=func, daemon=True)
    x.start()


def start_bot():
    db.connect()
    promo.start()
    bot = telebot.TeleBot(TOKEN)
    start_thread(get_config)

    users_status = {}
    users_question = {}
    users_secrets = {}
    users_trial_emails = {}

    def make_buttons(names, return_menu=True):
        markup = types.InlineKeyboardMarkup()
        for name in names:
            markup.add(types.InlineKeyboardButton(name, callback_data=md5(name.encode()).hexdigest()))
        if return_menu:
            markup.add(types.InlineKeyboardButton(RETURN_MENU_BUTTON,
                                                  callback_data=md5(RETURN_MENU_BUTTON.encode()).hexdigest()))
        return markup

    def make_buttons_row(names, width):
        markup = types.InlineKeyboardMarkup()
        for name in names:
            markup.add(types.InlineKeyboardButton(name, callback_data=md5(name.encode()).hexdigest()), width)
        return markup

    def menu_keyboard():
        markup = types.ReplyKeyboardMarkup(True, True)
        [markup.row(*row) for row in [[RANDOM_GIF_BUTTON_NAME, RECOVER_PASS_BUTTON_NAME],
                                      [PROMO_BUTTON_NAME, STORE_BUTTON_NAME], [PARTNERSHIP_BUTTON_NAME]]]
        return markup

    def is_email_valid(email):
        return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)

    def question_string(id):
        return list(QUESTIONS.keys())[users_question[id]]

    @bot.message_handler(commands=['start', 'help'])
    def start_command(message):
        bot.send_message(message.from_user.id, WELCOME_MESSAGE,
                         reply_markup=menu_keyboard())

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(message):
        if message.data == md5(RETURN_MENU_BUTTON.encode()).hexdigest():
            return_to_menu(message)
        elif any(md5(i.encode()).hexdigest() == message.data for i in promo.get_names()):
            promo_select(message)
        elif users_status[message.from_user.id] == USER_CHANGE_EMAIL:
            change_email_handle(message)
        else:
            answer_questions(message)
        bot.answer_callback_query(message.id)

    def return_to_menu(message):
        bot.send_message(message.from_user.id, RETURN_MENU_MESSAGE, reply_markup=menu_keyboard())

    def promo_select(message):
        promo.set_author_md5(message.data, message.from_user.id)
        bot.send_message(message.from_user.id, ENTER_PROMO_MESSAGE.format(
            author=promo.get_selected_name(message.from_user.id)), reply_markup=make_buttons([]))
        users_status[message.from_user.id] = USER_USE_PROMO

    def change_email_handle(message):
        if message.data == md5('Да'.encode()).hexdigest():
            enter_email_message_and_status(message)
        else:
            select_author(message)

    def add_if_not_there(dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = value

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        print(f'{message.from_user.id}: {message.text}')
        add_if_not_there(users_status, message.from_user.id, EMPTY)
        if message.text == RECOVER_PASS_BUTTON_NAME:
            bot.send_message(message.from_user.id, WRITE_YOUR_EMAIL_MESSAGE_RECOVERY, reply_markup=make_buttons([]))
        elif message.text == RANDOM_GIF_BUTTON_NAME:
            random_gif(message)
        elif message.text == PROMO_BUTTON_NAME:
            promo_button(message)
        elif message.text == STORE_BUTTON_NAME:
            store_button(message)
        elif message.text == PARTNERSHIP_BUTTON_NAME:
            partnership_reply(message)
        elif users_status[message.from_user.id] == USER_USE_PROMO:
            use_promo(message)
        elif users_status[message.from_user.id] == USER_PROMO_IDENTIFIER:
            promo_identifier_check(message)
        elif users_status[message.from_user.id] == USER_ENTER_EMAIL:
            enter_email(message)
        elif users_status[message.from_user.id] == USER_EMAIL_NOT_FOUND:
            email_not_found_support(message)
        elif '@' in message.text:
            password_recovery(message)

    def random_gif(message):
        bot.send_video(message.from_user.id, CUTIES[randint(0, len(CUTIES) - 1)],
                       reply_markup=menu_keyboard(), parse_mode='HTML')

    def promo_button(message):
        email = promo.get_saved_email(message.from_user.id)
        if email:
            bot.send_message(message.from_user.id, FOUND_YOUR_EMAIL_MESSAGE.format(email=email),
                             reply_markup=make_buttons(['Нет', 'Да']))
            users_status[message.from_user.id] = USER_CHANGE_EMAIL
        else:
            enter_email_message_and_status(message)

    def enter_email_message_and_status(message):
        bot.send_message(message.from_user.id, WRITE_YOUR_EMAIL_MESSAGE, reply_markup=make_buttons([]))
        users_status[message.from_user.id] = USER_ENTER_EMAIL

    def send_redirect_message(chat_id, message_text, button_text, url):
        buttons = types.InlineKeyboardMarkup()
        buttons.add(types.InlineKeyboardButton(button_text, url=url))
        buttons.add(types.InlineKeyboardButton(RETURN_MENU_BUTTON,
                                               callback_data=md5(RETURN_MENU_BUTTON.encode()).hexdigest()))
        return bot.send_message(chat_id, message_text, reply_markup=buttons)

    def store_button(message):
        send_redirect_message(message.from_user.id, 'Связаться с продавцом', 'Перейти',
                              f'https://t.me/{STORE_SELLER_ACC}')

    def partnership_reply(message):
        send_redirect_message(message.from_user.id, 'Сотрудничество', 'Сотрудничать', f'https://t.me/{PARTNERSHIP_ACC}')

    def enter_email(message):
        if not is_email_valid(message.text):
            email_is_not_valid(message)
            return

        if db.get_pass_by_email(message.text):
            promo.save_email(message.from_user.id, message.text)
            select_author(message)
        else:
            bot.send_message(message.from_user.id, TRY_AGAIN_MESSAGE)

    def select_author(message):
        users_status[message.from_user.id] = EMPTY
        bot.send_message(message.from_user.id, SELECT_AUTHOR_MESSAGE,
                         reply_markup=make_buttons(promo.get_names(), False))

    def password_recovery(message):
        if not is_email_valid(message.text):
            email_is_not_valid(message)
            return

        data = db.get_pass_by_email(message.text)
        if data:
            bot.send_message(message.from_user.id, ANSWER_QUESTIONS)
            users_question[message.from_user.id] = 0
            users_secrets[message.from_user.id] = (message.text, data)
            next_question(message)
        else:
            email_not_found_try_again_or_support(message)

    def email_not_found_try_again_or_support(message):
        if message.from_user.id not in users_trial_emails:
            bot.send_message(message.from_user.id, TRY_AGAIN_MESSAGE)
            users_trial_emails[message.from_user.id] = [message.text]
        else:
            bot.send_message(message.from_user.id, WRITE_YOUR_NICKNAME)
            users_status[message.from_user.id] = USER_EMAIL_NOT_FOUND
            users_trial_emails[message.from_user.id].append(message.text)

    def email_is_not_valid(message):
        bot.send_message(message.from_user.id, EMAIL_IS_NOT_VALID, reply_markup=make_buttons([]))

    def answer_questions(message):
        if is_answer_correct(message):
            bot.edit_message_reply_markup(message.message.chat.id, message.message.id, None)
            if users_question[message.from_user.id] != len(QUESTIONS) - 1:
                users_question[message.from_user.id] += 1
                next_question(message)
            else:
                send_password(message)
        else:
            bot.send_message(message.from_user.id, QUESTION_FAILURE_MESSAGE)

    def is_answer_correct(message):
        return \
            md5(list(QUESTIONS.values())[users_question[message.from_user.id]][1].encode()).hexdigest() == message.data

    def next_question(message):
        # users_question[message.from_user.id] += 1
        users_status[message.from_user.id] = USER_FINAL_QUESTION
        bot.send_message(message.from_user.id,
                         question_string(message.from_user.id),
                         reply_markup=make_buttons(
                             list(QUESTIONS.values())[users_question[message.from_user.id]][0], False),
                         parse_mode='HTML')

    def send_password(message):
        bot.send_message(message.from_user.id, SUCCESS, reply_markup=menu_keyboard())
        send_forgotten_pass(*users_secrets[message.from_user.id])
        delete_user(message.from_user.id)

    def delete_user(user_id):
        users_status.pop(user_id, None)
        users_question.pop(user_id, None)
        users_secrets.pop(user_id, None)
        users_trial_emails.pop(user_id, None)

    def email_not_found_support(message):
        mail.send(SUPPORT_EMAIL, f'USER: {message.text}',
                  f'EMAILS: {" ".join(users_trial_emails[message.from_user.id])}\n'
                  f'USER: {message.text}\n'
                  f'Telegram username: {message.from_user.username}')
        bot.send_message(message.from_user.id, GOT_LOGIN)
        delete_user(message.from_user.id)

    def use_promo(message):
        if promo.check_promo(message.from_user.id, message.text):
            users_status[message.from_user.id] = USER_PROMO_IDENTIFIER
            send_promo_identifier_message(message)
        else:
            bot.send_message(message.from_user.id, PROMO_FAILURE.format(
                author=promo.get_selected_name(message.from_user.id)))

    def send_promo_identifier_message(message):
        print(promo.get_user_promo_type(message.from_user.id))
        if promo.get_user_promo_type(message.from_user.id) == 'email':
            bot.send_message(message.from_user.id, WRITE_PROMO_IDENTIFIER_EMAIL, reply_markup=make_buttons([]))
        elif promo.get_user_promo_type(message.from_user.id) == 'phone':
            bot.send_message(message.from_user.id, WRITE_PROMO_IDENTIFIER_PHONE, reply_markup=make_buttons([]))

    def promo_identifier_check(message):
        promo.use_promo(promo.get_promo(message.from_user.id), promo.get_saved_email(message.from_user.id))
        send_promo_info(promo.get_saved_email(message.from_user.id),
                        promo.get_selected_name(message.from_user.id),
                        promo.get_promo(message.from_user.id),
                        message.text)
        promo.delete_info(message.from_user.id)
        bot.send_message(message.from_user.id, PROMO_SUCCESS, reply_markup=menu_keyboard())

    bot.infinity_polling()
