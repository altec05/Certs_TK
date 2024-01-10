import tkinter as tk
from tkinter import ttk
import sqlite3
import certs_db as db

import variables as var
from variables import path_db
import get_messages as mes
import service


# класс таблицы с её свойствами и созданием
class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        # выбор ячейки
        def selectItem(event):
            curItem = table.item(table.focus())
            col = table.identify_column(event.x)
            print(f'event:\n{event}')
            print(f'curItem:\n{curItem}')
            if curItem['values'] != '':
                if col == '#1':
                    cell_value = curItem['values'][0]
                elif col == '#2':
                    cell_value = curItem['values'][1]
                elif col == '#3':
                    cell_value = curItem['values'][2]
                elif col == '#4':
                    cell_value = curItem['values'][3]
                elif col == '#5':
                    cell_value = curItem['values'][4]
                elif col == '#6':
                    cell_value = curItem['values'][5]
                elif col == '#7':
                    cell_value = curItem['values'][6]
                elif col == '#8':
                    cell_value = curItem['values'][7]
                elif col == '#9':
                    cell_value = curItem['values'][8]
                elif col == '#10':
                    cell_value = curItem['values'][9]
                elif col == '#11':
                    cell_value = curItem['values'][10]
                elif col == '#12':
                    cell_value = curItem['values'][11]
                elif col == '#13':
                    cell_value = curItem['values'][12]
                elif col == '#14':
                    cell_value = curItem['values'][13]
                elif col == '#15':
                    cell_value = curItem['values'][14]
                elif col == '#16':
                    cell_value = curItem['values'][15]
                if cell_value != '':
                    var.temp_value = cell_value

        # выбор строки
        def item_selected(event):
            for selected_item in table.selection():
                item = table.item(selected_item)
                record = item['values']
                print(f'record:\n{record}')
                var.id_value = record[0]
                var.name_value = record[1]
                var.job_value = record[2]
                var.sn_value = record[3]
                var.start_value = record[4]
                var.end_value = record[5]
                var.uc_value = record[6]
                var.snils_value = record[7]
                var.inn_value = record[8]
                var.ogrn_value = record[9]
                var.city_value = record[10]
                var.tag_value_for_send = record[11]
                var.tag_value_list = var.tag_value_for_send.split(', ')
                var.briefing_value = record[12]
                var.last_test_number_value = record[13]
                var.last_test_date_value = record[14]
                var.note_value = record[15]

                temp = [record[0], record[1]]
                var.list_del_values.append(temp)

        table = ttk.Treeview(self, show="headings", selectmode="extended")
        table["columns"] = headings
        table["displaycolumns"] = headings

        # столбцы
        for head in headings:
            if 'ID' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_id(parent))
                table.column(head, anchor=tk.W, width=5)
            elif 'ФИО' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_name(parent))
                table.column(head, anchor=tk.W, width=225)
            elif 'Должность' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_job(parent))
                table.column(head, anchor=tk.W, width=200)
            elif 'Номер' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_sn(parent))
                table.column(head, anchor=tk.W, width=95)
            elif 'ОТ' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_st(parent))
                table.column(head, anchor=tk.CENTER, width=75)
            elif 'ДО' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_et(parent))
                table.column(head, anchor=tk.CENTER, width=75)
            elif 'УЦ' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_uc(parent))
                table.column(head, anchor=tk.CENTER, width=95)
            elif 'СНИЛС' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_snils(parent))
                table.column(head, anchor=tk.CENTER, width=35)
            elif 'ИНН' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_inn(parent))
                table.column(head, anchor=tk.CENTER, width=75)
            elif 'ОГРН' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_ogrn(parent))
                table.column(head, anchor=tk.CENTER, width=50)
            elif 'Город' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_city(parent))
                table.column(head, anchor=tk.CENTER, width=75)
            elif 'Метка' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_tag(parent))
                table.column(head, anchor=tk.CENTER, width=150)
            elif 'Инстр-ж' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_test(parent))
                table.column(head, anchor=tk.CENTER, width=70)
            elif '№ БТ' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_blank_test(parent))
                table.column(head, anchor=tk.W, width=70)
            elif 'Дата Т' in head:
                table.heading(head, text=head, anchor=tk.CENTER, command=lambda: sort_test_data(parent))
                table.column(head, anchor=tk.CENTER, width=75)
            else:
                table.heading(head, text=head, anchor=tk.CENTER)
                table.column(head, anchor=tk.W, width=120)
        # строки
        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrollYtable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrollYtable.set)
        scrollYtable.pack(side=tk.RIGHT, fill=tk.Y)

        scrollXtable = tk.Scrollbar(self, command=table.xview, orient=tk.HORIZONTAL)
        table.configure(xscrollcommand=scrollXtable.set)
        scrollXtable.pack(side=tk.BOTTOM, fill=tk.X)
        # бинды по клику
        table.bind('<<TreeviewSelect>>', item_selected)
        table.bind("<Button-1>", selectItem)

        table.pack(expand=tk.YES, fill=tk.BOTH)


# сортировка по ID сертификата по убыванию и возрастанию
def sort_id(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 1 or var.back_to_sort == False and var.temp_sort != 1 or var.back_to_sort == True and var.temp_sort != 1  and var.temp_sort != 2:
        head = 'ID ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
                print(data)
                for row in data:
                    print(row)
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY id ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=(head, 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 1
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 2 or var.back_to_sort == False and var.temp_sort != 2:
        head = 'ID v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY id DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=(head, 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 2
        var.back_to_sort = False


# сортировка по ФИО сертификата по убыванию и возрастанию
def sort_name(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 3 or var.back_to_sort == False and var.temp_sort != 3 or var.back_to_sort == True and var.temp_sort != 3 and var.temp_sort != 4:
        head = 'ФИО ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY name ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', head, 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 3
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 4 or var.back_to_sort == False and var.temp_sort != 4:
        head = 'ФИО v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY name DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', head, 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 4
        var.back_to_sort = False


# сортировка по должности сертификата по убыванию и возрастанию
def sort_job(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 5 or var.back_to_sort == False and var.temp_sort != 5 or var.back_to_sort == True and var.temp_sort != 5 and var.temp_sort != 6:
        head = 'Должность ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY job ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', head, 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 5
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 6 or var.back_to_sort == False and var.temp_sort != 6:
        head = 'Должность v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY job DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', head, 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 6
        var.back_to_sort = False


# сортировка по серийному номеру сертификата по убыванию и возрастанию
def sort_sn(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 7 or var.back_to_sort == False and var.temp_sort != 7 or var.back_to_sort == True and var.temp_sort != 7 and var.temp_sort != 8:
        head = 'Номер ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY serial_number ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', head, 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 7
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 8 or var.back_to_sort == False and var.temp_sort != 8:
        head = 'Номер v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY serial_number DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', head, 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 8
        var.back_to_sort = False


# сортировка по дате ОТ сертификата по убыванию и возрастанию
def sort_st(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 9 or var.back_to_sort == False and var.temp_sort != 9 or var.back_to_sort == True and var.temp_sort != 9 and var.temp_sort != 10:
        head = 'ОТ ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY start_time ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', head, 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 9
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 10 or var.back_to_sort == False and var.temp_sort != 10:
        head = 'ОТ v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY start_time DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', head, 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 10
        var.back_to_sort = False


# сортировка по дате ДО сертификата по убыванию и возрастанию
def sort_et(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 11 or var.back_to_sort == False and var.temp_sort != 11 or var.back_to_sort == True and var.temp_sort != 11 and var.temp_sort != 12:
        head = 'ДО ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY end_time ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', head, 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 11
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 12 or var.back_to_sort == False and var.temp_sort != 12:
        head = 'ДО v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY end_time DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', head, 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 12
        var.back_to_sort = False


# сортировка по УЦ сертификата по убыванию и возрастанию
def sort_uc(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 13 or var.back_to_sort == False and var.temp_sort != 13 or var.back_to_sort == True and var.temp_sort != 13 and var.temp_sort != 14:
        head = 'УЦ ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY uc ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', head, 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 13
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 14 or var.back_to_sort == False and var.temp_sort != 14:
        head = 'УЦ v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY uc DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', head, 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 14
        var.back_to_sort = False


# сортировка по СНИЛС сертификата по убыванию и возрастанию
def sort_snils(frame):
    service.clear_var_search_and_tag()
    print(var.back_to_sort, var.temp_sort)
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 15 or var.back_to_sort == False and var.temp_sort != 15 or var.back_to_sort == True and var.temp_sort != 15 and var.temp_sort != 16:
        print(var.back_to_sort, var.temp_sort)
        head = 'СНИЛС ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY snils ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', head,
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 15
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 16 or var.back_to_sort == False and var.temp_sort != 16:
        print(var.back_to_sort, var.temp_sort)
        head = 'СНИЛС v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY snils DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', head,
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 16
        var.back_to_sort = False


# сортировка по ИНН сертификата по убыванию и возрастанию
def sort_inn(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 17 or var.back_to_sort == False and var.temp_sort != 17 or var.back_to_sort == True and var.temp_sort != 17 and var.temp_sort != 18:
        head = 'ИНН ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY inn ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  head, 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 17
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 18 or var.back_to_sort == False and var.temp_sort != 18:
        head = 'ИНН v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY inn DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  head, 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 18
        var.back_to_sort = False


# сортировка по ОГРН сертификата по убыванию и возрастанию
def sort_ogrn(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 19 or var.back_to_sort == False and var.temp_sort != 19 or var.back_to_sort == True and var.temp_sort != 19 and var.temp_sort != 20:
        head = 'ОГРН ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY ogrn ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', head, 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 19
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 20 or var.back_to_sort == False and var.temp_sort != 20:
        head = 'ОГРН v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY ogrn DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', head, 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 20
        var.back_to_sort = False


# сортировка по Городу сертификата по убыванию и возрастанию
def sort_city(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 21 or var.back_to_sort == False and var.temp_sort != 21 or var.back_to_sort == True and var.temp_sort != 21 and var.temp_sort != 22:
        head = 'Город ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY city ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', head, 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 21
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 22 or var.back_to_sort == False and var.temp_sort != 22:
        head = 'Город v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY city DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', head, 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 22
        var.back_to_sort = False


# сортировка по Метке сертификата по убыванию и возрастанию
def sort_tag(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 23 or var.back_to_sort == False and var.temp_sort != 23 or var.back_to_sort == True and var.temp_sort != 23 and var.temp_sort != 24:
        head = 'Метка ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY tag ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', head, 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 23
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 24 or var.back_to_sort == False and var.temp_sort != 24:
        head = 'Метка v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY tag DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', head, 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 24
        var.back_to_sort = False


# сортировка по Прохождению инструктажа по убыванию и возрастанию
def sort_test(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 25 or var.back_to_sort == False and var.temp_sort != 25 or var.back_to_sort == True and var.temp_sort != 25 and var.temp_sort != 26:
        head = 'Инстр-ж ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY briefing ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', head, '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 25
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 26 or var.back_to_sort == False and var.temp_sort != 26:
        head = 'Инстр-ж v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY briefing DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', head, '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 26
        var.back_to_sort = False


# сортировка по № бланка тестирования по убыванию и возрастанию
def sort_blank_test(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 27 or var.back_to_sort == False and var.temp_sort != 27 or var.back_to_sort == True and var.temp_sort != 27 and var.temp_sort != 28:
        head = '№ БТ ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY last_test_number ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', head,
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 27
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 28 or var.back_to_sort == False and var.temp_sort != 28:
        head = '№ БТ v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY last_test_number DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', head,
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 28
        var.back_to_sort = False


# сортировка по дате тестирования по убыванию и возрастанию
def sort_test_data(frame):
    service.clear_var_search_and_tag()
    for widget in frame.winfo_children():
        widget.destroy()
    if var.back_to_sort == True and var.temp_sort == 29 or var.back_to_sort == False and var.temp_sort != 29 or var.back_to_sort == True and var.temp_sort != 29 and var.temp_sort != 30:
        head = 'Дата Т ^'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY last_test_date ASC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  head, 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 29
        var.back_to_sort = False
    elif var.back_to_sort == True and var.temp_sort == 30 or var.back_to_sort == False and var.temp_sort != 30:
        head = 'Дата Т v'
        if db.check_certs():
            data = ()
            if var.data_values:
                data = var.data_values
            else:
                with sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                    sqlite3.PARSE_COLNAMES) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY last_test_date DESC")
                    data = (row for row in cursor.fetchall())
            table = Table(frame, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  head, 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')
        var.temp_sort = 30
        var.back_to_sort = False