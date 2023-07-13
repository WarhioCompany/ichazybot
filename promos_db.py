import sqlite3 as sl

DATABASE_NAME = 'promocodes'
PROMO_DB = 'promo'
USERS_USED_DB = 'user_used'
USER_EMAILS = 'user_emails'


def connect_table():
    return sl.connect(f'{DATABASE_NAME}.db')


def create_db():
    create_table(PROMO_DB, f"""
                CREATE TABLE {PROMO_DB} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    promo TEXT,
                    confirmation TEXT
                );
            """)
    create_table(USERS_USED_DB, f"""
                    CREATE TABLE {USERS_USED_DB} (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        promo TEXT
                    );
                """)
    create_table(USER_EMAILS, f"""
                    CREATE TABLE {USER_EMAILS} (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        email TEXT
                    );
                """)


def create_table(table_name, table_scheme):
    con = connect_table()
    c = con.cursor()
    c.execute(f'''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ''')

    if c.fetchone()[0] != 1:
        with con:
            print(f'creating table {table_name}')
            con.execute(table_scheme)


def add_promos(promos):
    with connect_table() as con:
        con.executemany(f'INSERT INTO {PROMO_DB} (name, promo, confirmation) values (?, ?, ?)', promos)


def print_rows(name):
    with connect_table() as con:
        data = con.execute(f"SELECT * FROM {name}")
        for row in data:
            print(row)


def get_user_promo_type(name, promo):
    with connect_table() as con:
        return list(con.execute(f"SELECT confirmation FROM {PROMO_DB} WHERE name='{name}' AND promo='{promo}'"))[0][0]


def clear_table(name):
    with connect_table() as con:
        con.execute(f'DROP TABLE {name};')


def get_names():
    with connect_table() as con:
        return [i[0] for i in con.execute(f'SELECT name FROM {PROMO_DB}')]


def get_promos(name):
    with connect_table() as con:
        return [i[0] for i in con.execute(f"SELECT promo FROM {PROMO_DB} WHERE name='{name}'")]


def use_promo(email, promo):
    with connect_table() as con:
        con.execute(f'INSERT INTO {USERS_USED_DB} (email, promo) values (?, ?)', [email, promo])


def is_used(email, promo):
    with connect_table() as con:
        return (promo, ) in con.execute(f"SELECT promo FROM {USERS_USED_DB} WHERE email='{email}'")


def get_email(user):
    with connect_table() as con:
        res = [i for i in con.execute(f"SELECT email FROM {USER_EMAILS} WHERE user='{user}'")]
        return res[0][0] if res else []


def add_email(user, email):
    with connect_table() as con:
        con.execute(f'INSERT INTO {USER_EMAILS} (user, email) values (?, ?)', [user, email])


def test_values():
    add_promos([("Tinkoff", 'promo', 'email'), ("Влад A4", 'promo', 'phone'), ("Putin", 'promo', 'phone'),
                ("Porter Robinson", "promo", "email")])
