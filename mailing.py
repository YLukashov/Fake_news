import sqlite3


def check_user_in_base(user_id):
    try:
        sqlite_connection = sqlite3.connect('main_db/mail.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        info = cursor.execute('SELECT * FROM users WHERE id_telegram=?', (user_id, )).fetchone()
        #Если запрос вернул 0 строк, то...
        cursor.close()
        if info != None:
            return True
        else:
            return False

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def add_user(user_id):
    try:
        sqlite_connection = sqlite3.connect('main_db/mail.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = f"""INSERT INTO users
                                (id_telegram)
                                VALUES ({user_id});"""

        cursor.execute(sqlite_insert_with_param)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу users")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def del_user(user_id):
    try:
        sqlite_connection = sqlite3.connect('main_db/mail.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = f"""DELETE from users where id_telegram = {user_id};"""

        cursor.execute(sqlite_insert_with_param)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу users")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def get_users():
    try:
        sqlite_connection = sqlite3.connect('main_db/mail.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from users"""

        cursor.execute(sqlite_select_query)
        all_authors = cursor.fetchall()

        all_users = [i[1] for i in all_authors]
        return all_users

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

