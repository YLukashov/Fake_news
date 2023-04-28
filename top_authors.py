import sqlite3


def checklist():
    try:
        sqlite_connection = sqlite3.connect('main_db/confidence.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from authors"""
        cursor.execute(sqlite_select_query)
        all_authors = cursor.fetchall()

        book = dict()
        for i in range(len(all_authors)):
            book[all_authors[i][1]] = [all_authors[i][2], all_authors[i][3]]

        sorted_book = sorted(book.items(), key=lambda x: x[1][0])
        sorted_book.reverse()
        final_list = sorted_book[0:10]
        return final_list


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


# checklist()