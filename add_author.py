import sqlite3


def new_id():
    try:
        sqlite_connection = sqlite3.connect('main_db/confidence.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from authors"""
        cursor.execute(sqlite_select_query)
        all_authors = cursor.fetchall()

        cursor.close()

        return all_authors[-1][0] + 1

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def check_user_in_base(user_name):
    try:
        sqlite_connection = sqlite3.connect('main_db/confidence.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        info = cursor.execute('SELECT * FROM authors WHERE name=?', (user_name,)).fetchone()
        # Если запрос вернул 0 строк, то...
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


def add_user(name_au, fake_true):
    try:
        sqlite_connection = sqlite3.connect('main_db/confidence.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        if check_user_in_base(name_au):
            if fake_true:
                up = f"""UPDATE authors 
                    SET true_news = true_news + 1 
                    WHERE name = {name_au};"""
            else:
                up = f"""UPDATE authors 
                    SET fake_news = fake_news + 1 
                    WHERE name = '{name_au}';"""
            cursor.execute(up)
            sqlite_connection.commit()

        else:
            sqlite_insert_with_param = """INSERT INTO authors
                                    (id_author, name, true_news, fake_news)
                                    VALUES (?, ?, ?, ?);"""

            get_id = new_id()
            if fake_true:
                data_tuple = (get_id, name_au, 1, 0)
            else:
                data_tuple = (get_id, name_au, 0, 1)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу authors")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")