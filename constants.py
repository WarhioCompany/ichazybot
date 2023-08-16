import requests
import json
import time

# State
EMPTY = -1
# USER_FIRST_TRY = 0
# USER_SECOND_TRY = 1
USER_FINAL_QUESTION = 2
# USER_FINAL_QUESTION_SECOND_TRY = 3
USER_EMAIL_NOT_FOUND = 4
USER_ENTER_EMAIL = 5
USER_PROMO_IDENTIFIER = 6
USER_USE_PROMO = 7
USER_CHANGE_EMAIL = 8

SUPPORT_EMAIL = 'ichazybot@gmail.com'

# Bot

TOKEN = '5941370506:AAF3BglIIg6VlCP-Ppa0FiOPIC2bDf1O4SU'

# TEST TEST TEST TEST TEST !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TOKEN = '6098601821:AAHmo_e03absU9-1eFoTwsoJs0GX2_koLPk'

RANDOM_GIF_BUTTON_NAME = 'Милашка'
RECOVER_PASS_BUTTON_NAME = 'Восстановить пароль'
PROMO_BUTTON_NAME = 'Промокод'
STORE_BUTTON_NAME = 'Мерч'
PARTNERSHIP_BUTTON_NAME = 'Сотрудничество'

WELCOME_MESSAGE = 'Привет, я Чейзи. Я умею много чего, что ты выбираешь?'
WRITE_YOUR_EMAIL_MESSAGE_RECOVERY = 'Напиши свой email, указанный при регистрации в приложении'
TRY_AGAIN_MESSAGE = 'Я долго искал, такой почты нет нигде, попробуй еще раз'
WRITE_YOUR_NICKNAME = 'И сейчас ничего, это что, пранк? Напиши свой ник в приложении iChazy, наши архивные крыски хорошенько поищут'
GOT_LOGIN = 'Сейчас все проверим, и я свяжусь с тобой в телеге. Снюхаемся!'
ANSWER_QUESTIONS = 'Нашел тебя, но сперва ответь на проверочные вопросы'

WRITE_YOUR_EMAIL_MESSAGE = 'Напиши свой email, указанный при регистрации в приложении'
FOUND_YOUR_EMAIL_MESSAGE = 'Нашел твой email, хочешь изменить? {email}'
WRITE_PROMO_IDENTIFIER_EMAIL = 'Напиши свой email, указанный при регистрации промокода'
WRITE_PROMO_IDENTIFIER_PHONE = 'Напиши свой телефон, указанный при регистрации промокода'

SELECT_AUTHOR_MESSAGE = 'Выберите: '
ENTER_PROMO_MESSAGE = 'Ты выбрал {author}. У тебя есть промокодик?'
PROMO_SUCCESS = 'Круто! Скоро мы проверим '
PROMO_FAILURE = 'Ой, возможно какая то ошибка, не могу найти такого промокода у {author}'

STORE_SELECT_TYPE = '1) Футболка\n2) Стикер пак'
STORE_SELECT_COLOR = 'Выбери цвет'
STORE_SELECT_PRINT = 'Выбери принт'
STORE_SELECT_SIZE = 'Выбери цвет'
STORE_SELECT_STICKER_PACK_ID = 'Выбери стикерпак'

QUESTION_FAILURE_MESSAGE = "Соберись и попробуй еще раз!"
QUESTION_SECOND_FAILURE_MESSAGE = "Увы, но сегодня тебе не светит понежиться на веточках скидок и бонусов со мной, попробуй завтра"

SUCCESS = "Наконец-то я дождался тебя, залетай! Мои котики-секретари выслали тебе письмо на указанную почту."

CONFIG_PARSE_DELAY_SECONDS = 3600

QUESTIONS = {
    '''1. Какая награда была в челлендже #шаурмяу?''': (
    ['Шаурма', 'Уход за питомцем у грумера', 'Корм для котиков', 'Мерч iChazy'], 'Корм для котиков'),
    '''2. Какой бренд представлял челлендж #вжух?''': (
    ['Pampers', 'РЖД', 'Магазин магии Амаяка Акопяна', 'Lada'], 'Pampers'),
    '''3. Для чего в приложении iChazy нужны монеты?''': (
    ['Я смогу расплатиться ими в Пятерочке', 'Это мои пенсионные накопления', 'Они не настоящие?',
     'Для участия в челленджах с подарками'], 'Для участия в челленджах с подарками'),
    '''4. Что за милая мордашка изображена на нашем лого? Подсказка - не твоя 🦥''': (
    ['Каплевидный крот', 'Обыкновенный ленивец', 'Заболевший котик :(', 'Определенно кто-то из Зверополиса'],
    'Обыкновенный ленивец'),
}

CUTIES = ['https://tenor.com/ru/view/sloth-smile-slow-smooth-hd-neuron-activation-gif-24950071',
          'https://tenor.com/ru/view/sloth-gif-25476721',
          'https://tenor.com/ru/view/sloth-cute-smiling-happy-cute-animals-gif-17371126',
          'https://tenor.com/ru/view/sloth-gif-24452517', 'https://tenor.com/ru/view/smile-gif-23609977',
          'https://tenor.com/ru/view/curious-international-sloth-day-dude-smile-hi-gif-18805195',
          'https://tenor.com/ru/view/sleep-tired-nap-sloth-sloth-sanctuary-gif-15364610',
          'https://tenor.com/ru/view/munch-hungry-snack-cute-baby-gif-15364618',
          'https://tenor.com/ru/view/yawning-cute-sloth-climbing-hanging-on-gif-14146608',
          'https://tenor.com/ru/view/sleep-cuddle-nap-blanket-sloth-gif-15364617',
          'https://tenor.com/ru/view/sloth-wink-cute-side-eye-gif-16113780',
          'https://tenor.com/ru/view/scratch-itchy-cute-baby-sloth-gif-15364622',
          'https://tenor.com/ru/view/sloth-sleepy-tired-gif-5197827',
          'https://tenor.com/ru/view/eugene-sloths-playing-play-time-gif-12602378',
          'https://tenor.com/ru/view/scratch-itchy-smile-sloth-sloth-sanctuary-gif-15364632',
          'https://tenor.com/ru/view/funny-animals-gif-22379153',
          'https://tenor.com/ru/view/look-curious-sniff-cute-baby-gif-15364633',
          'https://tenor.com/ru/view/two-toed-sloth-and-three-gif-10774713',
          'https://tenor.com/ru/view/waving-fernando-the-sloth-cameo-sloth-hello-gif-17825162',
          'https://tenor.com/ru/view/yummy-international-sloth-day-baby-sloths-meal-chew-gif-18805185']


def make_config():
    config = {}
    config['TOKEN'] = TOKEN

    config['RANDOM_GIF_BUTTON_NAME'] = RANDOM_GIF_BUTTON_NAME
    config['RANDOM_GIF_BUTTON_NAME'] = RECOVER_PASS_BUTTON_NAME
    config['PROMO_BUTTON_NAME'] = PROMO_BUTTON_NAME
    config['STORE_BUTTON_NAME'] = STORE_BUTTON_NAME
    config['PARTNERSHIP_BUTTON_NAME'] = PARTNERSHIP_BUTTON_NAME

    config['WELCOME_MESSAGE'] = WELCOME_MESSAGE
    config['WRITE_YOUR_EMAIL_MESSAGE'] = WRITE_YOUR_EMAIL_MESSAGE_RECOVERY
    config['TRY_AGAIN_MESSAGE'] = TRY_AGAIN_MESSAGE
    config['WRITE_YOUR_NICKNAME'] = WRITE_YOUR_NICKNAME
    config['GOT_LOGIN'] = GOT_LOGIN
    config['ANSWER_QUESTIONS'] = ANSWER_QUESTIONS

    config['WRITE_YOUR_EMAIL_MESSAGE'] = WRITE_YOUR_EMAIL_MESSAGE
    config['FOUND_YOUR_EMAIL_MESSAGE'] = FOUND_YOUR_EMAIL_MESSAGE
    config['WRITE_PROMO_IDENTIFIER_EMAIL'] = WRITE_PROMO_IDENTIFIER_EMAIL
    config['WRITE_PROMO_IDENTIFIER_PHONE'] = WRITE_PROMO_IDENTIFIER_PHONE

    config['SELECT_AUTHOR_MESSAGE'] = SELECT_AUTHOR_MESSAGE
    config['ENTER_PROMO_MESSAGE'] = ENTER_PROMO_MESSAGE
    config['PROMO_SUCCESS'] = PROMO_SUCCESS
    config['PROMO_FAILURE'] = PROMO_FAILURE

    config['STORE_SELECT_TYPE'] = STORE_SELECT_TYPE
    config['STORE_SELECT_COLOR'] = STORE_SELECT_COLOR
    config['STORE_SELECT_PRINT'] = STORE_SELECT_PRINT
    config['STORE_SELECT_SIZE'] = STORE_SELECT_SIZE
    config['STORE_SELECT_STICKER_PACK_ID'] = STORE_SELECT_STICKER_PACK_ID

    config['QUESTION_FAILURE_MESSAGE'] = QUESTION_FAILURE_MESSAGE
    config['QUESTION_SECOND_FAILURE_MESSAGE'] = QUESTION_SECOND_FAILURE_MESSAGE

    config['SUCCESS'] = SUCCESS

    config['QUESTIONS'] = QUESTIONS

    config['CONFIG_PARSE_DELAY_SECONDS'] = CONFIG_PARSE_DELAY_SECONDS
    return config


def make_config_file():
    with open('config.json', 'w+', encoding='utf-8') as file:
        file.write(json.dumps(make_config(), indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))


def get_config():
    global TOKEN
    global RANDOM_GIF_BUTTON_NAME, RECOVER_PASS_BUTTON_NAME, PROMO_BUTTON_NAME, STORE_BUTTON_NAME, \
        PARTNERSHIP_BUTTON_NAME, WELCOME_MESSAGE, WRITE_YOUR_EMAIL_MESSAGE_RECOVERY, TRY_AGAIN_MESSAGE, \
        WRITE_YOUR_NICKNAME, GOT_LOGIN, ANSWER_QUESTIONS
    global WRITE_YOUR_EMAIL_MESSAGE, FOUND_YOUR_EMAIL_MESSAGE, WRITE_PROMO_IDENTIFIER_EMAIL, \
        WRITE_PROMO_IDENTIFIER_PHONE
    global SELECT_AUTHOR_MESSAGE, ENTER_PROMO_MESSAGE, PROMO_SUCCESS, PROMO_FAILURE
    global STORE_SELECT_TYPE, STORE_SELECT_COLOR, STORE_SELECT_PRINT, STORE_SELECT_SIZE, STORE_SELECT_STICKER_PACK_ID
    global QUESTION_FAILURE_MESSAGE, QUESTION_SECOND_FAILURE_MESSAGE
    global SUCCESS, QUESTIONS, CUTIES
    global CONFIG_PARSE_DELAY_SECONDS
    while True:
        start_time = time.time()
        print('Getting config....')

        config = json.loads(
            requests.get('https://raw.githubusercontent.com/WarhioCompany/ichazybot/main/config.json').text)

        print(config)

        TOKEN = config['TOKEN']

        RANDOM_GIF_BUTTON_NAME = config['RANDOM_GIF_BUTTON_NAME']
        RECOVER_PASS_BUTTON_NAME = config['RANDOM_GIF_BUTTON_NAME']
        PROMO_BUTTON_NAME = config['PROMO_BUTTON_NAME']
        STORE_BUTTON_NAME = config['STORE_BUTTON_NAME']
        PARTNERSHIP_BUTTON_NAME = config['PARTNERSHIP_BUTTON_NAME']

        WELCOME_MESSAGE = config['WELCOME_MESSAGE']
        WRITE_YOUR_EMAIL_MESSAGE_RECOVERY = config['WRITE_YOUR_EMAIL_MESSAGE']
        TRY_AGAIN_MESSAGE = config['TRY_AGAIN_MESSAGE']
        WRITE_YOUR_NICKNAME = config['WRITE_YOUR_NICKNAME']
        GOT_LOGIN = config['GOT_LOGIN']
        ANSWER_QUESTIONS = config['ANSWER_QUESTIONS']

        WRITE_YOUR_EMAIL_MESSAGE = config['WRITE_YOUR_EMAIL_MESSAGE']
        FOUND_YOUR_EMAIL_MESSAGE = config['FOUND_YOUR_EMAIL_MESSAGE']
        WRITE_PROMO_IDENTIFIER_EMAIL = config['WRITE_PROMO_IDENTIFIER_EMAIL']
        WRITE_PROMO_IDENTIFIER_PHONE = config['WRITE_PROMO_IDENTIFIER_PHONE']

        SELECT_AUTHOR_MESSAGE = config['SELECT_AUTHOR_MESSAGE']
        ENTER_PROMO_MESSAGE = config['ENTER_PROMO_MESSAGE']
        PROMO_SUCCESS = config['PROMO_SUCCESS']
        PROMO_FAILURE = config['PROMO_FAILURE']

        STORE_SELECT_TYPE = config['STORE_SELECT_TYPE']
        STORE_SELECT_COLOR = config['STORE_SELECT_COLOR']
        STORE_SELECT_PRINT = config['STORE_SELECT_PRINT']
        STORE_SELECT_SIZE = config['STORE_SELECT_SIZE']
        STORE_SELECT_STICKER_PACK_ID = config['STORE_SELECT_STICKER_PACK_ID']

        QUESTION_FAILURE_MESSAGE = config['QUESTION_FAILURE_MESSAGE']
        QUESTION_SECOND_FAILURE_MESSAGE = config['QUESTION_SECOND_FAILURE_MESSAGE']

        SUCCESS = config['SUCCESS']

        QUESTIONS = config['QUESTIONS']

        CONFIG_PARSE_DELAY_SECONDS = config['CONFIG_PARSE_DELAY_SECONDS']

        cuties = requests.get('https://raw.githubusercontent.com/WarhioCompany/ichazybot/main/cuties.txt').text
        CUTIES = cuties.split('\n')

        time.sleep(CONFIG_PARSE_DELAY_SECONDS - ((time.time() - start_time) % CONFIG_PARSE_DELAY_SECONDS))
