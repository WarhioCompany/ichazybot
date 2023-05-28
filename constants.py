import requests
import json
import time

# State
USER_FIRST_TRY = 0
USER_SECOND_TRY = 1
USER_FINAL_QUESTION = 2
USER_FINAL_QUESTION_SECOND_TRY = 3
USER_LOGIN = 4


SUPPORT_EMAIL = 'ichazybot@gmail.com'

# Bot

TOKEN = '5941370506:AAF3BglIIg6VlCP-Ppa0FiOPIC2bDf1O4SU'

RANDOM_GIF_BUTTON_NAME = 'Милашка'
RECOVER_PASS_BUTTON_NAME = 'Восстановить пароль'

WELCOME_MESSAGE = 'Привет, я Чейзи. Я умею быть миленьким или помогать восстанавливать пароль от аккаунта, что ты выбираешь?'
WRITE_YOUR_EMAIL_MESSAGE = 'Напиши свой email, указанный при регистрации в приложении'
TRY_AGAIN_MESSAGE = 'Я долго искал, такой почты нет нигде, попробуй еще раз'
WRITE_YOUR_NICKNAME = 'И сейчас ничего, это что, пранк? Напиши свой ник в приложении iChazy, наши архивные крыски хорошенько поищут'
GOT_LOGIN = 'Сейчас все проверим, и я свяжусь с тобой в телеге. Снюхаемся!'
ANSWER_QUESTIONS = 'Нашел тебя, но сперва ответь на проверочные вопросы'

QUESTION_FAILURE_MESSAGE = "Соберись и попробуй еще раз!"
QUESTION_SECOND_FAILURE_MESSAGE = "Увы, но сегодня тебе не светит понежиться на веточках скидок и бонусов со мной, попробуй завтра"

SUCCESS = "Наконец-то я дождался тебя, залетай! Мои котики-секретари выслали тебе письмо на указанную почту."

QUESTIONS = {
    '''1. Какая награда была в челлендже #шаурмяу?''': (['Шаурма', 'Уход за питомцем у грумера', 'Корм для котиков', 'Мерч iChazy'], 'Корм для котиков'),
    '''2. Какой бренд представлял челлендж #вжух?''': (['Pampers', 'РЖД', 'Магазин магии Амаяка Акопяна', 'Lada'], 'Pampers'),
    '''3. Для чего в приложении iChazy нужны монеты?''': (['Я смогу расплатиться ими в Пятерочке', 'Это мои пенсионные накопления', 'Они не настоящие?', 'Для участия в челленджах с подарками'], 'Для участия в челленджах с подарками'),
    '''4. Что за милая мордашка изображена на нашем лого? Подсказка - не твоя 🦥''': (['Каплевидный крот', 'Обыкновенный ленивец', 'Заболевший котик :(', 'Определенно кто-то из Зверополиса'], 'Обыкновенный ленивец'),
}

CUTIES = ['https://tenor.com/ru/view/sloth-smile-slow-smooth-hd-neuron-activation-gif-24950071', 'https://tenor.com/ru/view/sloth-gif-25476721', 'https://tenor.com/ru/view/sloth-cute-smiling-happy-cute-animals-gif-17371126', 'https://tenor.com/ru/view/sloth-gif-24452517', 'https://tenor.com/ru/view/smile-gif-23609977', 'https://tenor.com/ru/view/curious-international-sloth-day-dude-smile-hi-gif-18805195', 'https://tenor.com/ru/view/sleep-tired-nap-sloth-sloth-sanctuary-gif-15364610', 'https://tenor.com/ru/view/munch-hungry-snack-cute-baby-gif-15364618', 'https://tenor.com/ru/view/yawning-cute-sloth-climbing-hanging-on-gif-14146608', 'https://tenor.com/ru/view/sleep-cuddle-nap-blanket-sloth-gif-15364617', 'https://tenor.com/ru/view/sloth-wink-cute-side-eye-gif-16113780', 'https://tenor.com/ru/view/scratch-itchy-cute-baby-sloth-gif-15364622', 'https://tenor.com/ru/view/sloth-sleepy-tired-gif-5197827', 'https://tenor.com/ru/view/eugene-sloths-playing-play-time-gif-12602378', 'https://tenor.com/ru/view/scratch-itchy-smile-sloth-sloth-sanctuary-gif-15364632', 'https://tenor.com/ru/view/funny-animals-gif-22379153', 'https://tenor.com/ru/view/look-curious-sniff-cute-baby-gif-15364633', 'https://tenor.com/ru/view/two-toed-sloth-and-three-gif-10774713', 'https://tenor.com/ru/view/waving-fernando-the-sloth-cameo-sloth-hello-gif-17825162', 'https://tenor.com/ru/view/yummy-international-sloth-day-baby-sloths-meal-chew-gif-18805185']



def get_config():
    global TOKEN, RANDOM_GIF_BUTTON_NAME, RECOVER_PASS_BUTTON_NAME, WELCOME_MESSAGE, WRITE_YOUR_EMAIL_MESSAGE, TRY_AGAIN_MESSAGE, WRITE_YOUR_NICKNAME, GOT_LOGIN, ANSWER_QUESTIONS, QUESTION_FAILURE_MESSAGE, QUESTION_SECOND_FAILURE_MESSAGE, SUCCESS, QUESTIONS, CUTIES
    while True:
        starttime = time.time()

        config = json.loads(requests.get('https://raw.githubusercontent.com/WarhioCompany/ichazybot/main/config.json').text)

        TOKEN = config['TOKEN']
        RANDOM_GIF_BUTTON_NAME = config['RANDOM_GIF_BUTTON_NAME']
        RECOVER_PASS_BUTTON_NAME = config['RANDOM_GIF_BUTTON_NAME']
        WELCOME_MESSAGE = config['WELCOME_MESSAGE']
        WRITE_YOUR_EMAIL_MESSAGE = config['WRITE_YOUR_EMAIL_MESSAGE']
        TRY_AGAIN_MESSAGE = config['TRY_AGAIN_MESSAGE']
        WRITE_YOUR_NICKNAME = config['WRITE_YOUR_NICKNAME']
        GOT_LOGIN = config['GOT_LOGIN']
        ANSWER_QUESTIONS = config['ANSWER_QUESTIONS']
        QUESTION_FAILURE_MESSAGE = config['QUESTION_FAILURE_MESSAGE']
        QUESTION_SECOND_FAILURE_MESSAGE = config['QUESTION_SECOND_FAILURE_MESSAGE']
        SUCCESS = config['SUCCESS']
        QUESTIONS = config['QUESTIONS']

        delay = config['CONFIG_PARSE_DELAY_SECONDS']
        cuties = requests.get('https://raw.githubusercontent.com/WarhioCompany/ichazybot/main/cuties.txt').text
        CUTIES = cuties.split('\n')

        time.sleep(delay - ((time.time() - starttime) % delay))
