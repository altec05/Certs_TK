from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import os
import fsb795
import datetime
from datetime import datetime
import locale
from tkinter import filedialog

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


def check_path(path):
    # print(cert_path)
    if os.path.exists(path):
        label1['text'] = f'Путь существует!'
        return True
    else:
        label1['text'] = f'Путь не существует!'
        return False


def get_serts(get_path):
    # path = e_path.get()
    path = get_path
    if path != '':
        if check_path(path) == True:
            if path.endswith('.cer') == False:
                certs_folder_path = path
                # e_path.delete(0, END)

                folder_path = path
                certs = find_certs(folder_path)
                all_data = list()
                for cert in certs:
                    cert_name = cert
                    cert_path = folder_path + '\\' + cert_name

                    cert = fsb795.Certificate(cert_path)

                    name = get_name(cert)[0]
                    job = get_name(cert)[1]
                    snils = str(get_name(cert)[2])
                    inn = str(get_name(cert)[3])
                    start = get_date(cert)[0]
                    stop = get_date(cert)[1]
                    ogrn = str(get_name(cert)[4])

                    data = (name, job, get_sn(cert), start, stop, get_uc(cert), inn, snils, ogrn)
                    all_data.append(data)
                # print(len(all_data))
                # print(all_data)

                db = sqlite3.connect('../Certificates.sqlite')
                cursor = db.cursor()

                cursor.executemany(
                    "INSERT OR IGNORE INTO certs (name, job, serial_number, start_time, end_time, uc, inn, snils, ogrn"
                    ") VALUES(?,?, "
                    "?, ?, ?, ?, ?, ?, ?)",
                    all_data, )

                db.commit()
                label1['text'] = f'Сертификаты успешно добавлены в таблицу! Было обработано {len(all_data)} ' \
                                 f'сертификатов'
                db.close()
            else:
                all_data = list()

                cert = fsb795.Certificate(path)

                name = get_name(cert)[0]
                job = get_name(cert)[1]
                snils = str(get_name(cert)[2])
                inn = str(get_name(cert)[3])
                start = get_date(cert)[0]
                stop = get_date(cert)[1]
                ogrn = str(get_name(cert)[4])
                data = (name, job, get_sn(cert), start, stop, get_uc(cert), inn, snils, ogrn)
                all_data.append(data)

                # print(len(all_data))
                # print(all_data)

                db = sqlite3.connect('../Certificates.sqlite')
                cursor = db.cursor()

                cursor.executemany(
                    "INSERT OR IGNORE INTO certs (name, job, serial_number, start_time, end_time, uc, inn, snils, ogrn"
                    ") VALUES(?,?, "
                    "?, ?, ?, ?, ?, ?, ?)",
                    all_data, )

                db.commit()
                label1['text'] = f'Сертификат успешно добавлен в таблицу!'
                db.close()
        else:
            label1['text'] = f'Путь не существует!'
            # e_path.delete(0, END)
    else:
        label1['text'] = f'Введите путь!'
        # e_path.delete(0, END)


def get_name(cert):
    cn = ''
    job = ''
    snils = ''
    inn = ''
    ogrn = ''
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
        if key == 'OGRN':
            ogrn = sub[key]

    # label1['text'] = f'Субъект: {cn}\nДолжность: {job}\nСНИЛС: {snils}\nИНН: {inn}'
    return cn, job, snils, inn, ogrn


def get_date(cert):
    valid = cert.validityCert()
    start = valid["not_before"].date()
    end = valid["not_after"].date()


    # start = datetime.date(valid['not_after'].date())

    # label1['text'] = f'Действует с: {start.strftime("%x")}\nДействует по: {end.strftime("%x")}'

    # print(valid['not_after'].date(), type(valid['not_after']))
    # print(valid['not_before'].date())

    # print(start, type(start), type(start.strftime("%x")))

    # return start.strftime("%x"), end.strftime("%x")
    return start, end
    # return start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y")



def get_sn(cert):
    hex_output = decimal_to_hex(str(cert.serialNumber()))
    # e.delete(0, END)
    # e.insert(0, f'Серийный номер: {hex_output}')
    # label1['text'] = f'Серийный номер: {hex_output}'
    return hex_output


def decimal_to_hex(decimal_str):
    decimal_number = int(decimal_str, 10)
    hex_number = hex(decimal_number)
    # print(hex_number)

    n = len(hex_number)
    # print(hex_number[2:].zfill(n))
    return hex_number[2:].zfill(n)


def get_uc(cert):
    uc = ''
    iss, vlad_is = cert.issuerCert()
    # print('vlad_is=' + str(vlad_is))
    for key in iss.keys():
        # print(key + '=' + iss[key])
        if key == 'CN':
            uc = iss[key]
    # label1['text'] = f'Издатель: {uc}'
    return uc


def find_certs(folder):
    tree = os.walk(folder, topdown=True, onerror=None, followlinks=False)
    certs = []
    for root, directories, files in os.walk(folder):
        for file in files:
            if file.endswith('.cer') == False:
                continue
            else:
                if len(file) > 3:
                    certs.append(file)
                else:
                    continue
    return certs


def del_certs():
    db = sqlite3.connect('../Certificates.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE certs")
        db.commit()
        label1['text'] = "Таблица удалена!"
    except:
        label1['text'] = "Таблица не существует!"
    db.close()


def check_certs():
    db = sqlite3.connect('../Certificates.sqlite')
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM certs")
        res = cursor.fetchall()
        label1['text'] = f"Таблица Certs существует! Записей в таблице: {len(res)}"
        db.close()
        return True
    except:
        label1['text'] = "Таблица Certs не существует!"
        db.close()
        return False


def create_db():
    db = sqlite3.connect('../Certificates.sqlite')
    cursor = db.cursor()

    try:
        # cursor.execute('''CREATE TABLE IF NOT EXISTS certs (
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
            note TEXT
            )
            ''')
        db.commit()
        label1['text'] = f'Таблица успешно создана!'
        db.close()
    except:
        label1['text'] = f'Таблица уже существует!'
        db.close()


def open_file():
    if check_certs() == True:
        get_path = filedialog.askopenfilename(title="Выбор файла", filetypes=(("Сертификаты (*.cer)", "*.cer"),
                                                                              ("Все файлы", "*.*")))
        if get_path:
            # print(get_path)
            if check_certs():
                get_serts(get_path)
            else:
                label1['text'] = f'Таблица не существует!'
    else:
        label1['text'] = f'Таблица не существует!'


def open_dir():
    if check_certs() == True:
        get_path = filedialog.askdirectory()
        if get_path:
            # print(get_path)
            if check_certs():
                get_serts(get_path)
            else:
                label1['text'] = f'Таблица не существует!'
    else:
        label1['text'] = f'Таблица не существует!'


def show_table():
    for widget in f3.winfo_children():
        widget.destroy()

    if check_certs() == True:
        label1['text'] = f'Напоминание: Для автоширины нажмите на границу между названиями столбцов!'
        data = ()
        with sqlite3.connect('../Certificates.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM certs ORDER BY end_time")
            data = (row for row in cursor.fetchall())

        table = Table(f3, headings=('ID', 'ФИО', 'Должность', 'Серийный номер', 'От', 'До', 'УЦ', 'СНИЛС', 'ИНН',
                                      'ОГРН', 'Заметки'), rows=data)
        table.pack(expand=tk.YES, fill=tk.BOTH)
    else:
        label1['text'] = f'Таблица не существует!'

def sort_ogrn():
    for widget in f3.winfo_children():
        widget.destroy()

    if check_certs() == True:
        label1['text'] = f'Напоминание: Для автоширины нажмите на границу между названиями столбцов!'
        data = ()
        with sqlite3.connect('../Certificates.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM certs WHERE ogrn != '' ORDER BY name")
            data = (row for row in cursor.fetchall())

        table = Table(f3, headings=('ID', 'ФИО', 'Должность', 'Серийный номер', 'От', 'До', 'УЦ', 'СНИЛС', 'ИНН',
                                      'ОГРН', 'Заметки'), rows=data)
        table.pack(expand=tk.YES, fill=tk.BOTH)
    else:
        label1['text'] = f'Таблица не существует!'


def sort_name():
    for widget in f3.winfo_children():
        widget.destroy()

    if check_certs() == True:
        label1['text'] = f'Напоминание: Для автоширины нажмите на границу между названиями столбцов!'
        data = ()
        with sqlite3.connect('../Certificates.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM certs ORDER BY name")
            data = (row for row in cursor.fetchall())

        table = Table(f3, headings=('ID', 'ФИО', 'Должность', 'Серийный номер', 'От', 'До', 'УЦ', 'СНИЛС', 'ИНН',
                                      'ОГРН', 'Заметки'), rows=data)
        table.pack(expand=tk.YES, fill=tk.BOTH)
    else:
        label1['text'] = f'Таблица не существует!'


def sort_time():
    for widget in f3.winfo_children():
        widget.destroy()

    if check_certs() == True:
        label1['text'] = f'Напоминание: Для автоширины нажмите на границу между названиями столбцов!'
        data = ()
        with sqlite3.connect('../Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM certs ORDER BY end_time")

            data = (row for row in cursor.fetchall())

        table = Table(f3, headings=('ID', 'ФИО', 'Должность', 'Серийный номер', 'От', 'До', 'УЦ', 'СНИЛС', 'ИНН',
                                      'ОГРН', 'Заметки'), rows=data)
        table.pack(expand=tk.YES, fill=tk.BOTH)
    else:
        label1['text'] = f'Таблица не существует!'

def del_id():
    db = sqlite3.connect('../Certificates.sqlite')
    cursor = db.cursor()
    if e.get() != '':
        if e.get().isdigit():
            try:
                del_ID = e.get()
                sql_update_query = """DELETE FROM certs WHERE id = ?"""
                cursor.execute(sql_update_query, (del_ID,))
                db.commit()
                label1['text'] = f'Запись удалена из таблицы!'
                e.delete(0, END)
                db.close()
            except:
                label1['text'] = f'Ошибка удаления!'
                e.delete(0, END)
                db.close()
        else:
            label1['text'] = f'ID должен состоять только из цифр!'

    else:
        label1['text'] = f'Для удаления введите ID из таблицы!'

def print_width():
    print(root['width'])
    print(print(root.geometry()))

def open_win_edits():
    if check_certs() == True:
        def message(text):
            mb = messagebox.showerror(
                title='Ошибка',
                message=f'{text}'
            )

        def message_info(text):
            mb = messagebox.showinfo(
                title='Успех',
                message=f'{text}'
            )

        def get_query():
            if e_id.get() != '' and e_id.get().isdigit():
                id = e_id.get()
                sn = e_sn.get()
                note = e_note.get()
                send = list()
                send.append(int(id))
                if e_sn.get() != '':
                    sn = e_sn.get()
                    send.append(sn)
                if e_note.get() != '':
                    note = e_note.get()
                    send.append(note)
                print(send, type(send))
                print(len(send), send[0], type(send[0]))
                # return send
                return int(id), sn, note
            else:
                message('Некорректный ID!')

        def update_certs():
            send = list(get_query())

            try:
                if send[1] != '':
                    db = sqlite3.connect('../Certificates.sqlite')
                    cursor = db.cursor()
                    sql_sn_query = """UPDATE certs SET serial_number = ? WHERE id = ?"""
                    cursor.execute(sql_sn_query, (send[1], send[0]))
                    db.commit()
                    db.close()
                    message_info('Серийный номер обновлен!')
                if send[2] != '':
                    db = sqlite3.connect('../Certificates.sqlite')
                    cursor = db.cursor()
                    sql_sn_query = """UPDATE certs SET note = ? WHERE id = ?"""
                    cursor.execute(sql_sn_query, (send[2], send[0]))
                    db.commit()
                    db.close()
                    message_info('Заметка добавлена!')

                e_sn.delete(0, END)
                e_id.delete(0, END)
                e_note.delete(0, END)
            except:
                message('Ошибка обновления данных!')



        def show_table_win():
            for widget in f3.winfo_children():
                widget.destroy()

            if check_certs() == True:
                data = ()
                with sqlite3.connect('../Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY end_time")
                    data = (row for row in cursor.fetchall())

                table = Table(f3,
                              headings=('ID', 'ФИО', 'Должность', 'Серийный номер', 'От', 'До', 'УЦ', 'СНИЛС', 'ИНН',
                                        'ОГРН', 'Заметки'), rows=data)
                table.pack(expand=tk.YES, fill=tk.BOTH)
            else:
                message('Таблица не существует!')

        def find_table_win():
            print(win['width'])
            print(print(win.geometry()))

            for widget in f3.winfo_children():
                widget.destroy()

            if check_certs() == True:
                data = ()
                with sqlite3.connect('../Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    find = e_find.get().title()
                    sql_find_query = """SELECT * FROM certs WHERE name = ? ORDER BY name"""
                    cursor.execute(sql_find_query, (find,))

                    data = (row for row in cursor.fetchall())

                table = Table(f3,
                              headings=('ID', 'ФИО', 'Должность', 'Серийный номер', 'От', 'До', 'УЦ', 'СНИЛС', 'ИНН',
                                        'ОГРН', 'Заметки'), rows=data)
                table.pack(expand=tk.YES, fill=tk.BOTH)
            else:
                message('Таблица не существует!')

        win = Toplevel()
        win.geometry("1135x400+510+270")
        win.title('Изменение данных таблицы сертификатов')
        win.grab_set()
        root.resizable(True, True)
        root.minsize(1135, 400)

        f1 = Frame(win)
        f1.pack(fill=X, padx=10, pady=10)

        f2 = Frame(win)
        f2.pack(fill=X, padx=10, pady=10)

        f3 = Frame(win, bg='black')
        f3.pack(fill=BOTH, expand=True, padx=10, pady=10)

        btn_show_table = Button(f1, text='Вывод таблицы', command=show_table_win, padx=10, pady=5)
        btn_show_table.pack(side=LEFT)

        e_find = Entry(f1, width=50)
        e_find.pack(padx=10, side=RIGHT)

        btn_find = Button(f1, text='Найти по ФИО', command=find_table_win, padx=10, pady=5)
        btn_find.pack(side=RIGHT)

        label_win_id = Label(f2, text='Изменить для ID', bg='#cfcfcf',
                             fg='black')
        label_win_id.pack(side=LEFT, fill=X)

        e_id = Entry(f2, width=10)
        e_id.pack(padx=10, side=LEFT)

        label_win_sn = Label(f2, text='серийный номер на', bg='#cfcfcf',
                             fg='black')
        label_win_sn.pack(side=LEFT, fill=X)

        e_sn = Entry(f2, width=40)
        e_sn.pack(padx=10, side=LEFT)

        label_win_note = Label(f2, text='и/или добавить заметку', bg='#cfcfcf',
                               fg='black')
        label_win_note.pack(side=LEFT, fill=X)

        e_note = Entry(f2, width=50)
        e_note.pack(padx=10, side=LEFT)

        btn_save = Button(f2, text='Обновить', command=update_certs, padx=10, pady=5)
        btn_save.pack(side=LEFT)
    else:
        label1['text'] = f'Таблица не существует!'



root = Tk()
root.title('Менеджер сертификатов')
root.geometry('1000x600+500+200')
# 672x600+641+318
root.resizable(True, True)
root.minsize(960, 300)

main_menu = Menu(root)
root.config(menu=main_menu)

# Table certs
table_menu = Menu(main_menu, tearoff=0)
table_menu.add_command(label="Создать таблицу", command=create_db)
table_menu.add_command(label="Удалить таблицу", command=del_certs)
table_menu.add_command(label="Проверить существование таблицы", command=check_certs)
# table_menu.add_command(label="Вывод размера окна", command=print_width)
table_menu.add_command(label="Изменить данные в таблице", command=open_win_edits)
main_menu.add_cascade(label="Таблица", menu=table_menu)

# File
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="Выбрать сертификат", command=open_file)
file_menu.add_command(label="Выбрать папку", command=open_dir)
main_menu.add_cascade(label="Задать путь", menu=file_menu)



f1 = Frame(root)
f1.pack(fill=X, padx=10, pady=10)

f2 = Frame(root)
f2.pack(fill=X, padx=10, pady=10)

f3 = Frame(root, bg='black')
f3.pack(fill=BOTH, expand=True, padx=10, pady=10)

label1 = Label(f1, text='Для начала работы выберите действие во вкладках меню вверху.', bg='#cfcfcf', fg='black')
label1.pack(side=TOP, fill=X)

btn_show_table = Button(f2, width=15, text='Вывод таблицы', command=show_table, padx=10, pady=5)
btn_show_table.pack(side=LEFT)

btn_ogrn = Button(f2, width=15, text='Есть ОГРН', command=sort_ogrn, padx=10, pady=5)
btn_ogrn.pack(side=RIGHT)

btn_sort_name = Button(f2, width=25, text='Сортировка по ФИО', command=sort_name, padx=10, pady=5)
btn_sort_name.pack(side=RIGHT)

btn_sort_time = Button(f2, width=25, text='Сортировка по дате окончания', command=sort_time, padx=10, pady=5)
btn_sort_time.pack(side=RIGHT)

e=Entry(f2)
e.pack(padx=10, side=RIGHT)

btn_del_id = Button(f2, text='Удалить ID', command=del_id, padx=10, pady=5)
btn_del_id.pack(side=RIGHT)

root.mainloop()
