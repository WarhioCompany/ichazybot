from sshtunnel import SSHTunnelForwarder
import sshtunnel
import logging
import psycopg2 as pg

creds = {
    "PG_UN": "ichazy_user",
    "PG_DB_NAME": "ichazy",
    "PG_DB_PW": "hsZcpCKCnVHpgSmZ7ezDvoNapSBJP4g57",
    "SSH_PKEY": '?R"+<g6y=@UI~59-HzcN{<Ge_n~A5dn">moo',
    "SSH_HOST": "91.206.15.234",
    "DB_HOST": "91.206.15.234",
    "LOCALHOST": "127.0.0.1",
    "PORT": "5432"
}
cur = None
conn = None


def connect():
    global cur

    sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    ssh_tunnel = SSHTunnelForwarder(
        (creds['SSH_HOST'], 22),
        ssh_username='app',
        ssh_password=creds['SSH_PKEY'],
        remote_bind_address=('127.0.0.1', 5432)
    )
    ssh_tunnel.start()

    conn = pg.connect(
        host='127.0.0.1',
        port=ssh_tunnel.local_bind_port,
        user=creds["PG_UN"],
        password=creds["PG_DB_PW"],
        database=creds["PG_DB_NAME"]
    )
    conn.autocommit = True

    cur = conn.cursor()


def request_sql(sql):
    cur.execute(sql)
    return cur.fetchall()


def get_pass_by_email(email):
    data = request_sql(f'''select data->'secret' from ichazy.users_auth where primary_id='{email}';''')
    if not data:
        return False
    return data[0][0]


def close():
    conn.commit()
    conn.close()
