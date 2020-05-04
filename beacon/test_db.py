import sqlite3
from sqlite3 import Error
from . import settings


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
    return c.lastrowid


def create_user(conn, task):
    sql = """ INSERT INTO
            login(name,token,authorization,count_req)
            VAlUES(?,?,?,0) """
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def print_table(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM login")
        print(cur.fetchall())


def request_permission(conn, username, password):
    cur = conn.cursor()
    user = cur.execute("SELECT * FROM login WHERE token = ?", [username]).fetchall()
    if len(user) > 0:
        for use in user:
            if use[2] == password:
                return use[3]
        return 0
    return -1


def main():
    sql_create_login_table = """CREATE TABLE IF NOT EXISTS login (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                token text NOT NULL,
                                authorization integer NOT NULL,
                                count_req integer
                            );"""

    conn = create_connection(settings.PATH_LOGIN)

    create_table(conn, sql_create_login_table)
    with conn:
        user1 = ("Bob", "12345", 3)
        user2 = ("Perry", "Auto", 2)
        user3 = ("Ted", "Alligator3", 1)

        create_user(conn, user1)
        create_user(conn, user2)
        create_user(conn, user3)
        print_table(conn)


if __name__ == "__main__":
    main()
