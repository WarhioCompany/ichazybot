import promos_db as db
from hashlib import md5


user_data = {}


def start():
    db.create_db()


def get_names():
    return db.get_names()


def set_author_md5(md5_name, user):
    author_name = [i for i in get_names() if md5(i.encode()).hexdigest() == md5_name][0]
    print(f'User selected {author_name}')
    user_data[user] = {'author': author_name}


def get_selected_name(user):
    return user_data[user]['author'] if user in user_data else None


def check_promo(user, promo):
    if is_promo_valid(user, promo):
        user_data[user]['promo'] = promo
        return True
    else:
        return False


def use_promo(promo, email):
    db.use_promo(email, promo)


def get_user_promo_type(user):
    return db.get_user_promo_type(user_data[user]['author'], user_data[user]['promo'])


def delete_info(user):
    del user_data[user]


def get_saved_email(user):
    return db.get_email(user)


def get_promo(user):
    return user_data[user]['promo']


def save_email(user, email):
    db.add_email(user, email)


def is_promo_valid(user, promo):
    return promo in db.get_promos(user_data[user]['author'])