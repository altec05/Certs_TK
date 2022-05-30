from tkinter import *
import sqlite3
import os
import fsb795
import datetime
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

cert_name = r'\Выдра Ольга Петровна 2023 Казначейство.cer'
cert_path = r'C:\Users\DomashenkoIK\Desktop\1' + cert_name

cert = fsb795.Certificate(cert_path)


def create_db():
    db = sqlite3.connect('../Certificates.sqlite')
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS certs (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    job TEXT NOT NULL,
    serial_number TEXT NOT NULL UNIQUE,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    uc TEXT NOT NULL,
    snils TEXT NOT NULL,
    inn TEXT NOT NULL,
    note TEXT
    )
    ''')
    db.commit()
    label1['text'] = f'Таблица успешно создана!'
    db.close()


def check_path():
    # print(cert_path)
    if os.path.exists(cert_path):
        label1['text'] = f'Путь существует!'
        return True
    else:
        label1['text'] = f'Путь не существует!'
        return False


def decimal_to_hex(decimal_str):
    decimal_number = int(decimal_str, 10)
    hex_number = hex(decimal_number)
    # print(hex_number)

    n = len(hex_number)
    # print(hex_number[2:].zfill(n))
    return hex_number[2:].zfill(n)


def get_sn():
    hex_output = decimal_to_hex(str(cert.serialNumber()))
    label1['text'] = f'Серийный номер: {hex_output}'
    return hex_output


def get_name():
    cn = ''
    job = ''
    snils = ''
    inn = ''
    sub, vlad_sub = cert.subjectCert()
    # print('vlad_sub=' + str(vlad_sub))
    for key in sub.keys():
        # print(key + '=' + sub[key])
        if key == 'CN':
            cn = sub[key]
        if key == 'title':
            job = sub[key]
        if key == 'SNILS':
            snils = sub[key]
        if key == 'INN':
            inn = sub[key]

    label1['text'] = f'Субъект: {cn}\nДолжность: {job}\nСНИЛС: {snils}\nИНН: {inn}'
    return cn, job, snils, inn


def get_uc():
    uc = ''
    iss, vlad_is = cert.issuerCert()
    # print('vlad_is=' + str(vlad_is))
    for key in iss.keys():
        # print(key + '=' + iss[key])
        if key == 'CN':
            uc = iss[key]
    label1['text'] = f'Издатель: {uc}'
    return uc


def get_date():
    valid = cert.validityCert()
    start = valid["not_before"].date()
    end = valid["not_after"].date()

    # start = datetime.date(valid['not_after'].date())
    label1['text'] = f'Действует с: {start.strftime("%x")}\nДействует по: {end.strftime("%x")}'
    # print(valid['not_after'].date(), type(valid['not_after']))
    # print(valid['not_before'].date())
    return start.strftime("%x"), end.strftime("%x")


def check_certs():
    db = sqlite3.connect('../Certificates.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM certs")
        label1['text'] = "Таблица Certs существует!"
        res = cursor.fetchall()

        print(res, sep='\n', end='\n')
        db.close()
        return True
    except:
        label1['text'] = "Таблица Certs не существует!"
        db.close()
        return False


def del_certs():
    db = sqlite3.connect('../Certificates.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE certs")
        db.commit()
        label1['text'] = "Таблица удалена!"
    except:
        label1['text'] = "Таблица не удалена!"
    db.close()


def send_data():
    db = sqlite3.connect('../Certificates.sqlite')
    cursor = db.cursor()

    name = get_name()[0]
    job = get_name()[1]
    snils = str(get_name()[2])
    inn = str(get_name()[3])
    start = get_date()[0]
    stop = get_date()[1]

    data = [(name, job, get_sn(), start, stop, get_uc(), inn, snils)]
    print(data)
    try:
        cursor.executemany(
            "INSERT INTO certs (name, job, serial_number, start_time, end_time, uc, inn, snils) VALUES(?,?, ?, ?, ?, ?, ?, ?)",
            data, )

        db.commit()
        label1['text'] = f'Запрос успешно отправлен в БД!'
    except:
        label1['text'] = f'Ошибка отправки запроса!'
    db.close()


root = Tk()
root.title('Менеджер сертификатов')
root.geometry('600x400+500+200')
root.resizable(False, False)

btn_create = Button(root, text='Создать таблицу Certs', command=create_db)
btn_create.configure(width=25)
btn_create.pack()

btn_check_tab = Button(root, text='Проверить наличие таблицы Certs', command=check_certs)
btn_check_tab.configure(width=25)
btn_check_tab.pack()

btn_del = Button(root, text='Удалить таблицу Certs', command=del_certs)
btn_del.configure(width=25)
btn_del.pack()

btn_check_path = Button(root, text='Проверка пути сертификата', command=check_path)
btn_check_path.configure(width=25)
btn_check_path.pack()

btn_get_sn = Button(root, text='Получение серийного номера', command=get_sn)
btn_get_sn.configure(width=25)
btn_get_sn.pack()

btn_get_cn = Button(root, text='Получение субъекта', command=get_name)
btn_get_cn.configure(width=25)
btn_get_cn.pack()

btn_get_uc = Button(root, text='Получение издателя', command=get_uc)
btn_get_uc.configure(width=25)
btn_get_uc.pack()

btn_get_date = Button(root, text='Получение срока действия сетификата', command=get_date)
btn_get_date.configure(width=25)
btn_get_date.pack()

btn_get_date = Button(root, text='Отправить сертификат в БД', command=send_data)
btn_get_date.configure(width=25)
btn_get_date.pack()

label1 = Label(root, text='')
label1.pack()

root.mainloop()

create_db()