import os
import sqlite3
import get_messages
from variables import path_db
import variables as var


# Проверка запрашиваемого пути
def check_path(ch_path):
    if os.path.exists(ch_path):
        return True
    else:
        return False


# Проверка пути для файла БД
def create_path(cr_path):
    if not (os.path.exists(cr_path)):
        os.makedirs(cr_path, exist_ok=True)


# Проверка существования таблицы по запросу
def click_check_tab():
    if check_certs():
        db = sqlite3.connect(path_db + '/Certificates.sqlite')
        cursor = db.cursor()

        try:
            cursor.execute("SELECT * FROM certs")
            res = cursor.fetchall()
            get_messages.info('Проверка таблицы', f'Таблица "Сертификаты" существует!\nЗаписей в таблице: {len(res)}')
            db.close()
        except:
            get_messages.error('Проверка таблицы', f'Таблица "Сертификаты" не существует!')
            db.close()
    else:
        get_messages.error('Проверка таблицы', f'Таблица "Сертификаты" не существует!')


# Проверка существования таблицы "Сертификаты"
def check_certs():
    if not (os.path.exists(path_db)):
        create_db()

    db = sqlite3.connect(path_db + '/Certificates.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM certs")
        db.close()
        return True
    except:
        db.close()
        return False
    finally:
        db.close()


# Создать таблицу в БД
def create_db():
    if not check_certs():
        # Создаем путь для БД
        create_path(path_db)

        # Создаем и подключаемся к БД
        db = sqlite3.connect(path_db + '/Certificates.sqlite')
        cursor = db.cursor()

        try:
            cursor.execute('''CREATE TABLE certs (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            job TEXT,
                            serial_number TEXT NOT NULL UNIQUE,
                            start_time DATE NOT NULL,
                            end_time DATE NOT NULL,
                            uc TEXT NOT NULL,
                            snils TEXT NOT NULL,
                            inn TEXT NOT NULL,
                            ogrn TEXT,                                                                    
                            city TEXT NOT NULL,
                            tag TEXT,
                            briefing BOOLEAN,
                            last_test_number INTEGER,
                            last_test_date DATE, 
                            note TEXT
                            )
                            ''')

            db.commit()
            db.close()
            get_messages.info('Создание таблицы', 'Таблица создана!')

        except:
            db.close()
            get_messages.error('Создание таблицы', 'Ошибка создания таблицы!')
        finally:
            db.close()
    else:
        get_messages.error('Создание таблицы', 'Ошибка: таблица уже существует!')


# Очистить таблицу "Сертификаты" в БД
def clear_db():
    if check_certs():
        db = sqlite3.connect(path_db + '/Certificates.sqlite')
        cursor = db.cursor()
        cursor.execute("DELETE FROM certs")
        db.commit()
        db.close()
        get_messages.info('Очистка таблицы', 'Таблица успешно очищена!')
    else:
        get_messages.error('Очистка таблицы', 'Таблица "Сертификаты" не существует и не может быть очищена!')


# Удалить таблицу из БД
def del_certs():
    if check_certs():
        db = sqlite3.connect(path_db + '/Certificates.sqlite')
        cursor = db.cursor()
        try:
            cursor.execute("DROP TABLE certs")
            db.commit()
            get_messages.info('Удаление таблицы', 'Таблица успешно удалена!')
        except:
            get_messages.error('Удаление таблицы', 'Ошибка удаления таблицы!')
        db.close()
    else:
        get_messages.error('Удаление таблицы', 'Ошибка: таблица "Сертификаты" не существует!')


# удалить запись в БД
def del_id(id_value):
    db = sqlite3.connect(path_db + '/Certificates.sqlite')
    cursor = db.cursor()
    if id_value != '':
        if check_id(id_value):
            try:
                del_ID = id_value
                sql_update_query = """DELETE FROM certs WHERE id = ?"""
                cursor.execute(sql_update_query, (del_ID,))
                db.commit()
                db.close()
                var.id_value = ''
                # get_messages.info('Удаление записи', 'Запись успешно удалена!')
                return True
            except:
                var.id_value = ''
                get_messages.error('Удаление записи', 'Ошибка: запись не может быть удалена!')
                db.close()
                return False
        else:
            var.id_value = ''
            get_messages.error('Поиск значения в таблице', 'Ошибка: Введенный ID не зарегистрирован!')
    else:
        get_messages.error('Поиск значения в таблице', 'Ошибка: Для удаления выберите значение из таблицы!')


# проверка существования записи в БД
def check_id(id_check):
    db = sqlite3.connect(path_db + '/Certificates.sqlite')
    cursor = db.cursor()

    try:
        sql_check_id_query = """SELECT * FROM certs WHERE id = ?"""
        cursor.execute(sql_check_id_query, (id_check,))
        count = cursor.fetchall()
        if len(count) > 0:
            db.close()
            return True
        else:
            db.close()
            return False
    except:
        db.close()
        get_messages.error('Поиск значения в таблице', 'Ошибка: запись не найдена!')
