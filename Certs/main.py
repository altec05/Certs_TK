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
    serial_number TEXT NOT NULL,
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    uc TEXT NOT NULL,
    snils TEXT NOT NULL,
    inn TEXT NOT NULL,
    note TEXT
    )
    ''')

    db.close()


def check_path():
    print(cert_path)
    if os.path.exists(cert_path):
        label1['text'] = f'Путь существует!'
    else:
        label1['text'] = f'Путь не существует!'


def decimal_to_hex(decimal_str):
    decimal_number = int(decimal_str, 10)
    hex_number = hex(decimal_number)
    print(hex_number)

    ###################
    n = len(hex_number)
    print(hex_number[2:].zfill(n))
    return hex_number[2:].zfill(n)
    # return hex_number
    ###################


def get_sn():
    hex_output = decimal_to_hex(str(cert.serialNumber()))
    label1['text'] = f'Серийный номер: {hex_output}'


def get_name():
    cn = ''
    title = ''
    snils = ''
    inn = ''
    sub, vlad_sub = cert.subjectCert()
    print('vlad_sub=' + str(vlad_sub))
    for key in sub.keys():
        print(key + '=' + sub[key])
        if key == 'CN':
            cn = sub[key]
        if key == 'title':
            title = sub[key]
        if key == 'SNILS':
            snils = sub[key]
        if key == 'INN':
            inn = sub[key]

    label1['text'] = f'Субъект: {cn}\nДолжность: {title}\nСНИЛС: {snils}\nИНН: {inn}'

def get_uc():
    cn = ''
    iss, vlad_is = cert.issuerCert()
    print('vlad_is=' + str(vlad_is))
    for key in iss.keys():
        print(key + '=' + iss[key])
        if key == 'CN':
            cn = iss[key]
    label1['text'] = f'Издатель: {cn}'

def get_date():
    valid = cert.validityCert()
    start = valid["not_before"].date()
    end = valid["not_after"].date()

    # start = datetime.date(valid['not_after'].date())
    label1['text'] = f'Действует с: {start.strftime("%x")}\nДействует по: {end.strftime("%x")}'
    # print(valid['not_after'].date(), type(valid['not_after']))
    # print(valid['not_before'].date())


root = Tk()
root.title('Менеджер сертификатов')
root.geometry('600x400+500+200')
root.resizable(False, False)

btn_check_path = Button(root, text='Проверка пути сертификата', command=check_path)
btn_check_path.configure(width=25)
btn_check_path.pack()

btn_get = Button(root, text='Получение серийного номера', command=get_sn)
btn_get.configure(width=25)
btn_get.pack()

btn_get = Button(root, text='Получение субъекта', command=get_name)
btn_get.configure(width=25)
btn_get.pack()

btn_get = Button(root, text='Получение издателя', command=get_uc)
btn_get.configure(width=25)
btn_get.pack()

btn_get = Button(root, text='Получение срока действия сетификата', command=get_date)
btn_get.configure(width=25)
btn_get.pack()

label1 = Label(root, text='')
label1.pack()

root.mainloop()

create_db()
