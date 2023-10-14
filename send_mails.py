import mail
from constants import const


def send_forgotten_pass(email, password):
    mail.send(email, 'Ваш пароль. IChazy',
              f"""
                              Похоже вы забыли ваш пароль.
                              Ваш пароль: {password}
                              """)


def send_forgotten_email(nickname, emails, telegram_username):
    mail.send(const['SUPPORT_EMAIL'], f'USER: {nickname}',
              f'EMAILS: {" ".join(emails)}\n'
              f'USER: {nickname}\n'
              f'Telegram username: {telegram_username}')


# chazy email, telegram?, promo_author, promo, identification c
def send_promo_info(ichazy_email, promo_author, promo, identification):
    mail.send(const['SUPPORT_EMAIL'], f'{promo_author} PROMO ({promo})',
              f'IChazy email: {ichazy_email}\n'
              f'Identification: {identification}\n'
              f'{promo_author}: {promo}')
