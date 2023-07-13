users_info = {}


def add_user(user):
    users_info[user] = {}


def set_shirt_color(user, color):
    users_info[user]['color'] = color


def set_shirt_size(user, size):
    users_info[user]['size'] = size


def set_shirt_print(user, print_id):
    users_info[user]['print_id'] = print_id


def set_sticker_pack_id(user, sticker_pack_id):
    users_info[user]['sticker_pack_id'] = sticker_pack_id
