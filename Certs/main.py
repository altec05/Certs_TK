#-*-coding: UTF-8 -*-
# пакеты
from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox
import datetime
from tkinter import ttk
import os

# модули программы
import certs_db as db
import get_messages as mes
import service
import variables as var
from variables import path_db
import add_certs as add
import table_win
import edit_cert
import tags


def root_closing():
    # Флаг для завершения процесса
    var.exit_flag = True

    # Закрытие окон
    root.destroy()
    root.quit()


def start_search():
    clear_tag_filter()
    search_for_name()


def clear_search():
    e_search.delete(0, END)
    var.find_row = ''
    var.need_find = False
    var.temp_search_sort = 0
    var.back_to_search_sort = False
    var.local_sort = False
    print('Очистил поиск')


# Функция поиска по части ФИО
def search_for_name():
    def show_results(results):
        data = (row for row in results)

        table = table_win.Table(f3, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                              'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                              'Дата Т', 'Примечание'), rows=data)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        if not var.local_sort:
            mes.warning('Результаты поиска', f'Найдено подходящих записей: {len(results)}')

    def get_results(find_sub_row, where_find, step):
        sort = ''
        if var.back_to_search_sort:
            if var.temp_search_sort == 0:
                sort = 'name'
            elif var.temp_search_sort == 1:
                sort = 'id ASC'
            elif var.temp_search_sort == 2:
                sort = 'id DESC'
            elif var.temp_search_sort == 3:
                sort = 'name ASC'
            elif var.temp_search_sort == 4:
                sort = 'name DESC'
            elif var.temp_search_sort == 5:
                sort = 'job ASC'
            elif var.temp_search_sort == 6:
                sort = 'job DESC'
            elif var.temp_search_sort == 7:
                sort = 'serial_number ASC'
            elif var.temp_search_sort == 8:
                sort = 'serial_number DESC'
            elif var.temp_search_sort == 9:
                sort = 'start_time ASC'
            elif var.temp_search_sort == 10:
                sort = 'start_time DESC'
            elif var.temp_search_sort == 11:
                sort = 'end_time ASC'
            elif var.temp_search_sort == 12:
                sort = 'end_time DESC'
            elif var.temp_search_sort == 13:
                sort = 'uc ASC'
            elif var.temp_search_sort == 14:
                sort = 'uc DESC'
            elif var.temp_search_sort == 15:
                sort = 'snils ASC'
            elif var.temp_search_sort == 16:
                sort = 'snils DESC'
            elif var.temp_search_sort == 17:
                sort = 'inn ASC'
            elif var.temp_search_sort == 18:
                sort = 'inn DESC'
            elif var.temp_search_sort == 19:
                sort = 'ogrn ASC'
            elif var.temp_search_sort == 20:
                sort = 'ogrn DESC'
            elif var.temp_search_sort == 21:
                sort = 'city ASC'
            elif var.temp_search_sort == 22:
                sort = 'city DESC'
            elif var.temp_search_sort == 23:
                sort = 'tag ASC'
            elif var.temp_search_sort == 24:
                sort = 'tag DESC'
            elif var.temp_search_sort == 25:
                sort = 'briefing ASC'
            elif var.temp_search_sort == 26:
                sort = 'briefing DESC'
            elif var.temp_search_sort == 27:
                sort = 'last_test_number ASC'
            elif var.temp_search_sort == 28:
                sort = 'last_test_number DESC'
            elif var.temp_search_sort == 29:
                sort = 'last_test_date ASC'
            elif var.temp_search_sort == 30:
                sort = 'last_test_date DESC'
        else:
            sort = 'name'

        db1 = sqlite3.connect(path_db + '/Certificates.sqlite',
                              detect_types=sqlite3.PARSE_DECLTYPES |
                                           sqlite3.PARSE_COLNAMES)
        cursor = db1.cursor()
        print(where_find)
        need_find = ''
        if step == 1:
            # По ФИО
            need_find = str(find_sub_row).title()
        elif step == 2:
            # По серийному номеру
            need_find = str(find_sub_row).upper()
        elif step == 3:
            # По должности
            need_find = str(find_sub_row).capitalize()
        # Общий поиск
        sql_search_query = f"""SELECT * FROM certs WHERE {where_find} LIKE '%{need_find}%' ORDER BY {sort}"""
        print(sql_search_query)
        cursor.execute(sql_search_query)
        finded_rows = cursor.fetchall()
        print(finded_rows)
        result = list()
        data = ()
        for row in finded_rows:
            result.append(row)
        # Дополнительно для серийника добавляем 00 в начало
        if step == 2:
            need_find = '00' + str(need_find)
            sql_search_query = f"""SELECT * FROM certs WHERE {where_find} LIKE '%{need_find}%' ORDER BY {sort}"""
            print(sql_search_query)
            cursor.execute(sql_search_query)
            finded_rows = cursor.fetchall()
            print(finded_rows)
            data = ()
            for row in finded_rows:
                result.append(row)
        # Дополнительно для серийника убираем 00 в начале
        if step == 2:
            if str(need_find)[0:2] == '00':
                need_find = need_find[2:]
                sql_search_query = f"""SELECT * FROM certs WHERE {where_find} LIKE '%{need_find}%' ORDER BY {sort}"""
                print(sql_search_query)
                cursor.execute(sql_search_query)
                finded_rows = cursor.fetchall()
                print(finded_rows)
                data = ()
                for row in finded_rows:
                    result.append(row)
        # Дополнительно для серийника добавляем 0 в начало
        if step == 2:
            need_find = '0' + str(need_find)
            sql_search_query = f"""SELECT * FROM certs WHERE {where_find} LIKE '%{need_find}%' ORDER BY {sort}"""
            print(sql_search_query)
            cursor.execute(sql_search_query)
            finded_rows = cursor.fetchall()
            print(finded_rows)
            data = ()
            for row in finded_rows:
                result.append(row)
        # Дополнительно для серийника убираем 0 в начале
        if step == 2:
            if str(need_find)[0:1] == '0':
                need_find = need_find[1:]
                sql_search_query = f"""SELECT * FROM certs WHERE {where_find} LIKE '%{need_find}%' ORDER BY {sort}"""
                print(sql_search_query)
                cursor.execute(sql_search_query)
                finded_rows = cursor.fetchall()
                print(finded_rows)
                data = ()
                for row in finded_rows:
                    result.append(row)
        db1.close()
        return result

    def find_sub_row_in_bd(find_sub_row):
        clear_frame()

        if db.check_certs():
            send_data = list()
            first_search = get_results(find_sub_row, 'name', 1)
            second_search = get_results(find_sub_row, 'serial_number', 2)
            third_search = get_results(find_sub_row, 'job', 3)
            var.back_to_search_sort = False
            if len(first_search) > 0:
                send_data += first_search
            if len(second_search) > 0:
                send_data += second_search
            if len(third_search) > 0:
                send_data += third_search
            # Очищаем результаты от повторений по id
            for row in send_data:
                # Ищем все индексы вхождений id в список
                indeces = [i for i in range(len(send_data)) if send_data[i] == row]
                rev_indxs = list()
                # Если больше 1 раза id
                if len(indeces) > 1:
                    # Переворачиваем индексы для удаления без смещений с конца к началу
                    for i in indeces[::-1]:
                        rev_indxs.append(i)
                    # Удаляем по индексу из списка
                    for i in rev_indxs[:len(rev_indxs)-1]:
                        print(f'Удаляем {send_data[i]} по {i}')
                        del send_data[i]
            return send_data
        else:
            mes.error('Поиск в БД', 'Ошибка: таблица не существует!')

    if not var.back_to_search_sort:
        var.temp_search_sort = 0

    if e_search.get() != '':
        if var.find_row != '':
            if var.find_row == e_search.get():
                show_results(find_sub_row_in_bd(var.find_row))
            else:
                var.find_row = str(e_search.get())
                show_results(find_sub_row_in_bd(var.find_row))
        else:
            var.find_row = str(e_search.get())
            show_results(find_sub_row_in_bd(var.find_row))
    else:
        if var.find_row != '':
            if var.find_row == e_search.get():
                show_results(find_sub_row_in_bd(var.find_row))
            else:
                var.find_row = str(e_search.get())
                show_results(find_sub_row_in_bd(var.find_row))
        else:
            var.find_row = str(e_search.get())
            show_results(find_sub_row_in_bd(var.find_row))


# если таблица существует, то сбрасываем временные переменные и показываем таблицу
def reload():
    # Если есть флаг полного выхода, то не выполняем
    # Для функции изменения записи с закрытием
    # При закрытии окна до подтверждения
    if not var.exit_flag:
        if db.check_certs():
            # var.temp_sort = 0
            var.id_value = ''
            if var.need_find:
                e_search.delete(0, END)
                e_search.insert(0, var.find_row)
                search_for_name()
            elif var.back_to_tag_filter_sort:
                show_only_tag('')
            else:
                show_table()


# если таблица существует, то сбрасываем временные переменные и показываем таблицу
def full_reload():
    if db.check_certs():
        var.temp_sort = 0
        var.id_value = ''
        var.list_del_values.clear()
        var.back_to_sort = False
        var.find_row = ''
        var.need_find = False
        var.temp_search_sort = 0
        var.back_to_search_sort = False
        e_search.delete(0, END)
        show_table()
        clear_tag_filter()
        clear_var_search_and_tag()
        var.local_sort = False


# Очистка временных переменных поиска и фильтрации с очисткой поля
def clear_var_search_and_tag():
    service.clear_var_search_and_tag()
    clear_tag_filter()
    # clear_search()


# Очистка поля выбора фильтра после сброса
def clear_tag_filter():
    reload()
    if cb_filter_tag.current() != '':
        cb_filter_tag.set('Выберите метку')
        var.temp_tag_value = ''
        var.temp_tag_sort_value = 0
        var.back_to_tag_filter_sort = False
        var.local_sort = False
        print('Очистил фильтр')


# Заполнение КБ с метками и его обновление перед открытием
def fill_cb_before_open():
    tags.fill_cb_from_file(tags.tag_file_wr())
    cb_filter_tag['values'] = var.tags_list_value
    print(var.tags_list_value)
    cb_filter_tag.current(0)


# Вывод по метке
def show_only_tag(event):
    def show_tag(tag_list):
        if len(tag_list) > 0:
            clear_frame()
            data = (row for row in tag_list)

            table = table_win.Table(f3, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if not var.local_sort:
                mes.info('Фильтр по тегу', f'Сертификатов, с запрашиваемым тегом: {len(tag_list)}')
        else:
            mes.warning("Фильтр по тегу", "Не найдено сертификатов с запрашиваемым тегом.")

    def find_tag(tag):
        print(f'tag:\n{tag}')
        if db.check_certs():
            sort = ''
            if var.back_to_tag_filter_sort:
                if var.temp_tag_sort_value == 0:
                    sort = 'tag'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 1:
                    sort = 'id ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 2:
                    sort = 'id DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 3:
                    sort = 'name ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 4:
                    sort = 'name DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 5:
                    sort = 'job ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 6:
                    sort = 'job DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 7:
                    sort = 'serial_number ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 8:
                    sort = 'serial_number DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 9:
                    sort = 'start_time ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 10:
                    sort = 'start_time DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 11:
                    sort = 'end_time ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 12:
                    sort = 'end_time DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 13:
                    sort = 'uc ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 14:
                    sort = 'uc DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 15:
                    sort = 'snils ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 16:
                    sort = 'snils DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 17:
                    sort = 'inn ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 18:
                    sort = 'inn DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 19:
                    sort = 'ogrn ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 20:
                    sort = 'ogrn DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 21:
                    sort = 'city ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 22:
                    sort = 'city DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 23:
                    sort = 'tag ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 24:
                    sort = 'tag DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 25:
                    sort = 'briefing ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 26:
                    sort = 'briefing DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 27:
                    sort = 'last_test_number ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 28:
                    sort = 'last_test_number DESC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 29:
                    sort = 'last_test_date ASC'
                    var.back_to_tag_filter_sort = False
                elif var.temp_tag_sort_value == 30:
                    sort = 'last_test_date DESC'
                    var.back_to_tag_filter_sort = False
            else:
                sort = 'name ASC'
            db1 = sqlite3.connect(path_db + '/Certificates.sqlite')
            cursor = db1.cursor()
            sql_update_query = f"""SELECT * FROM certs ORDER BY {sort}"""
            cursor.execute(sql_update_query)
            tag_certs = cursor.fetchall()
            tag_list = list()
            for cert in tag_certs:
                tag_cert = cert[11]
                if tag in tag_cert:
                    tag_list.append(cert)
            db1.close()
            return tag_list
        else:
            mes.error('Фильтр по тегу', 'Ошибка: таблица не существует!')
    if not var.back_to_tag_filter_sort:
        var.temp_tag_sort_value = 0
    var.temp_tag_value = cb_filter_tag.get()
    show_tag(find_tag(cb_filter_tag.get()))
    clear_search()


# Переход к изменению сертификата с передачей временных переменных, полученных из модуля tab_win при нажатии на строку
def edit_table():
    if var.id_value != '':
        # e_search.delete(0, END)
        data = [var.id_value, var.name_value, var.job_value, var.sn_value, var.tag_value_for_send, var.briefing_value,
                var.last_test_number_value, var.last_test_date_value, var.note_value]
        edit_cert.edit_value(root, data, reload)
        # data = [var.id_value, var.name_value, var.job_value, var.sn_value, var.start_value,
        #         var.end_value, var.uc_value, var.snils_value, var.inn_value, var.ogrn_value, var.tag_value_for_send,
        #         var.briefing_value, var.last_test_number_value, var.last_test_date_value, var.note_value]
        # edit_cert.edit_value(root, data, reload)
        root.withdraw()
    else:
        pass


# изменение записи по двойному клику
def edit_table_ev(event):
    if var.id_value != '':
        # e_search.delete(0, END)
        data = [var.id_value, var.name_value, var.job_value, var.sn_value, var.tag_value_for_send, var.briefing_value,
                var.last_test_number_value, var.last_test_date_value, var.note_value]
        edit_cert.edit_value(root, data, reload)
        root.withdraw()
    else:
        pass


# очистка фрейма, содержащего таблицу для её обновления
def clear_frame():
    for widget in f3.winfo_children():
        widget.destroy()
    label_count_of_certs['text'] = ''


def sort_search_id():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 1:
            var.temp_search_sort = 1
        else:
            var.temp_search_sort = 2
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 1:
            var.temp_tag_sort_value = 1
        else:
            var.temp_tag_sort_value = 2
        show_only_tag('')


def sort_search_name():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 3:
            var.temp_search_sort = 3
        else:
            var.temp_search_sort = 4
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 3:
            var.temp_tag_sort_value = 3
        else:
            var.temp_tag_sort_value = 4
        show_only_tag('')


def sort_search_job():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 5:
            var.temp_search_sort = 5
        else:
            var.temp_search_sort = 6
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 5:
            var.temp_tag_sort_value = 5
        else:
            var.temp_tag_sort_value = 6
        show_only_tag('')


def sort_search_sn():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 7:
            var.temp_search_sort = 7
        else:
            var.temp_search_sort = 8
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 7:
            var.temp_tag_sort_value = 7
        else:
            var.temp_tag_sort_value = 8
        show_only_tag('')


def sort_search_st():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 9:
            var.temp_search_sort = 9
        else:
            var.temp_search_sort = 10
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 9:
            var.temp_tag_sort_value = 9
        else:
            var.temp_tag_sort_value = 10
        show_only_tag('')


def sort_search_et():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 11:
            var.temp_search_sort = 11
        else:
            var.temp_search_sort = 12
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 11:
            var.temp_tag_sort_value = 11
        else:
            var.temp_tag_sort_value = 12
        show_only_tag('')


def sort_search_uc():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 13:
            var.temp_search_sort = 13
        else:
            var.temp_search_sort = 14
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 13:
            var.temp_tag_sort_value = 13
        else:
            var.temp_tag_sort_value = 14
        show_only_tag('')


def sort_search_snils():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 15:
            var.temp_search_sort = 15
        else:
            var.temp_search_sort = 16
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 15:
            var.temp_tag_sort_value = 15
        else:
            var.temp_tag_sort_value = 16
        show_only_tag('')


def sort_search_inn():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 17:
            var.temp_search_sort = 17
        else:
            var.temp_search_sort = 18
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 17:
            var.temp_tag_sort_value = 17
        else:
            var.temp_tag_sort_value = 18
        show_only_tag('')


def sort_search_ogrn():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 19:
            var.temp_search_sort = 19
        else:
            var.temp_search_sort = 20
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 19:
            var.temp_tag_sort_value = 19
        else:
            var.temp_tag_sort_value = 20
        show_only_tag('')


def sort_search_city():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 21:
            var.temp_search_sort = 21
        else:
            var.temp_search_sort = 22
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 21:
            var.temp_tag_sort_value = 21
        else:
            var.temp_tag_sort_value = 22
        show_only_tag('')


def sort_search_tag():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 23:
            var.temp_search_sort = 23
        else:
            var.temp_search_sort = 24
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 23:
            var.temp_tag_sort_value = 23
        else:
            var.temp_tag_sort_value = 24
        show_only_tag('')


def sort_search_test():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 25:
            var.temp_search_sort = 25
        else:
            var.temp_search_sort = 26
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 25:
            var.temp_tag_sort_value = 25
        else:
            var.temp_tag_sort_value = 26
        show_only_tag('')


def sort_search_blank_test():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 27:
            var.temp_search_sort = 27
        else:
            var.temp_search_sort = 28
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 27:
            var.temp_tag_sort_value = 27
        else:
            var.temp_tag_sort_value = 28
        show_only_tag('')


def sort_search_test_data():
    var.local_sort = True
    if var.find_row != '':
        clear_frame()
        var.back_to_search_sort = True
        if var.temp_search_sort != 29:
            var.temp_search_sort = 29
        else:
            var.temp_search_sort = 30
        search_for_name()
    elif var.temp_tag_value != '':
        clear_frame()
        var.back_to_tag_filter_sort = True
        if var.temp_tag_sort_value != 29:
            var.temp_tag_sort_value = 29
        else:
            var.temp_tag_sort_value = 30
        show_only_tag('')


# сортировка по ID сертификата по убыванию и возрастанию
def sort_id():
    clear_frame()
    table_win.sort_id(f3)


# сортировка по ФИО сертификата по убыванию и возрастанию
def sort_name():
    clear_frame()
    table_win.sort_name(f3)


# сортировка по должности сертификата по убыванию и возрастанию
def sort_job():
    clear_frame()
    table_win.sort_job(f3)


# сортировка по серийному номеру сертификата по убыванию и возрастанию
def sort_sn():
    clear_frame()
    table_win.sort_sn(f3)


# сортировка по дате ОТ сертификата по убыванию и возрастанию
def sort_st():
    clear_frame()
    table_win.sort_st(f3)


# сортировка по дате ДО сертификата по убыванию и возрастанию
def sort_et():
    clear_frame()
    table_win.sort_et(f3)


# сортировка по Удостоверяющему центру сертификата по убыванию и возрастанию
def sort_uc():
    clear_frame()
    table_win.sort_uc(f3)


# сортировка по СНИЛС сертификата по убыванию и возрастанию
def sort_snils():
    clear_frame()
    table_win.sort_snils(f3)


# сортировка по ИНН сертификата по убыванию и возрастанию
def sort_inn():
    clear_frame()
    table_win.sort_inn(f3)


# сортировка по ОГРН сертификата по убыванию и возрастанию
def sort_ogrn():
    clear_frame()
    table_win.sort_ogrn(f3)


# сортировка по Городу сертификата по убыванию и возрастанию
def sort_city():
    clear_frame()
    table_win.sort_city(f3)


# сортировка по Метке сертификата по убыванию и возрастанию
def sort_tag():
    clear_frame()
    table_win.sort_tag(f3)


# сортировка по Прохождению инструктажа по убыванию и возрастанию
def sort_test():
    clear_frame()
    table_win.sort_test(f3)


# сортировка по № бланка тестирования по убыванию и возрастанию
def sort_blank_test():
    clear_frame()
    table_win.sort_blank_test(f3)


# сортировка по дате тестирования по убыванию и возрастанию
def sort_test_data():
    clear_frame()
    table_win.sort_test_data(f3)


# копируем серийный номер, ФИО, должность, город выделенной записи
def copy_cert_serialnumber_name_job_city():
    root.clipboard_clear()
    temp_row = var.name_value + ' ' + var.sn_value + ' ' + var.job_value + ' ' + var.city_value
    root.clipboard_append(temp_row)
    mes.info('Копирование записи', f'Для записи № {var.id_value} скопированы данные:\n'
                                   f'ФИО, Серийный номер, должность, город.')
    var.id_value = ''


# копируем ФИО, должность, город выделенной записи
def copy_cert_name_job_city():
    root.clipboard_clear()
    temp_row = var.name_value + ' ' + var.job_value + ' ' + var.city_value
    root.clipboard_append(temp_row)
    mes.info('Копирование записи', f'Для записи № {var.id_value} скопированы данные:\n'
                                   f'ФИО, должность, город.')
    var.id_value = ''


# копируем серийный номер выделенной записи
def copy_cert():
    root.clipboard_clear()
    root.clipboard_append(var.sn_value)
    mes.info('Копирование записи', f'Серийный номер записи № {var.id_value} скопирован.')
    var.id_value = ''


# копируем выбранную ячейку
def copy_cert_col():
    if var.temp_value != '':
        root.clipboard_clear()
        root.clipboard_append(var.temp_value)
        mes.info('Копирование ячейки', f'Значение "{var.temp_value}" из записи № {var.id_value} скопировано.')
        var.temp_value = ''
    else:
        mes.warning('Копирование ячейки', f'Значение не скопировано так как ячейка пуста.\nЕсли ячейка не пуста, '
                                          f'то повторно нажмите на ячейку и выберите копирование.')


# Удалить закончившиеся сертификаты
def delete_old_certs():
    if db.check_certs():
        now = datetime.date.today()

        db1 = sqlite3.connect(path_db + '/Certificates.sqlite',
                              detect_types=sqlite3.PARSE_DECLTYPES |
                                           sqlite3.PARSE_COLNAMES)
        cursor = db1.cursor()
        sql_update_query = """SELECT * FROM certs ORDER BY end_time"""
        cursor.execute(sql_update_query)
        date_certs = cursor.fetchall()
        db1.close()
        near = list()
        for cert in date_certs:
            date_cert = cert[5]
            period = date_cert - now
            if period.days < 0:
                near.append(cert)
        if not len(near) > 0:
            mes.info("Удаление истекших сертификатов", "Не обнаружено сертификатов с истекшим сроком действия!")
        else:
            question = messagebox.askokcancel(title='Удаление истекших сертификатов', message=f'Вы уверены, что'
                                                                                              f' хотите удалить'
                                                                                              f' {len(near)}'
                                                                                              f' сертификатов?')
            if question:
                for cert in near:
                    if db.del_id(cert[0]):
                        var.id_value = ''
                reload()


# Функция проверки истекающих сертификатов
def show_date():
    def show_near(near):
        if len(near) > 0:
            data = (row for row in near)

            table = table_win.Table(f3, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            mes.warning('Проверка сроков сертификатов', f'Сертификатов, срок действия которых истекает: {len(near)}')
        else:
            mes.info("Проверка сроков сертификатов", "Не найдено сертификатов с истекающим сроком действия.")

    def check_near():
        clear_frame()

        if db.check_certs():
            now = datetime.date.today()

            db1 = sqlite3.connect(path_db + '/Certificates.sqlite',
                                  detect_types=sqlite3.PARSE_DECLTYPES |
                                               sqlite3.PARSE_COLNAMES)
            cursor = db1.cursor()
            sql_update_query = """SELECT * FROM certs ORDER BY end_time"""
            cursor.execute(sql_update_query)
            date_certs = cursor.fetchall()
            near = list()
            data = ()
            for cert in date_certs:
                date_cert = cert[5]
                period = date_cert - now
                if period.days < 35:
                    near.append(cert)
            db1.close()
            return near
        else:
            mes.error('Проверка сроков сертификатов', 'Ошибка: таблица не существует!')

    show_near(check_near())


# Выдача уведомления об истекающих сертификатах
def check_near_info():
    if db.check_certs():
        now = datetime.date.today()

        db1 = sqlite3.connect(path_db + '/Certificates.sqlite',
                              detect_types=sqlite3.PARSE_DECLTYPES |
                                           sqlite3.PARSE_COLNAMES)
        cursor = db1.cursor()
        sql_update_query = """SELECT * FROM certs ORDER BY end_time"""
        cursor.execute(sql_update_query)
        date_certs = cursor.fetchall()
        near = list()
        data = ()
        for cert in date_certs:
            date_cert = cert[5]
            period = date_cert - now
            if period.days < 35:
                near.append(cert)
        if len(near) > 0:
            mes.warning("Истечение срока действия сертификатов", "Внимание!\nОбнаружены сертификаты, срок действия "
                                                                 f"которых заканчивается: {len(near)}")
        db1.close()


# удалить выбранную запись
def delete_id():
    question = ''
    items = ''
    if len(var.list_del_values) > 1:
        print(f'Список элементов на удаление: {var.list_del_values}')
        print(f'Отсортированный список элементов на удаление: {var.list_del_values.sort()}')
        if len(var.list_del_values) > 2 or len(var.list_del_values) == 2 and var.list_del_values[0][0] == var.list_del_values[1][0]:
            for item in var.list_del_values:
                indexes = [i for i in range(len(var.list_del_values)) if var.list_del_values[i] == item]
                print(f'Элемент: {item} и индексы: {item}')
                print(item, indexes)
                rev_indxs = indexes[::-1]
                print(rev_indxs)
                rev_indxs = rev_indxs[0:len(rev_indxs)-1]
                print(rev_indxs)
                for ind in rev_indxs:
                    print(f'Удаляем {var.list_del_values[ind]} по {ind}')
                    del var.list_del_values[ind]

        for item in var.list_del_values:
            row = '№ ' + str(item[0]) + ' "' + str(item[1]) + '"\n'
            items += row

        question = messagebox.askokcancel(title='Удаление записей', message=f'Вы уверены, что хотите удалить указанные записи?:\n\n'
                                                                           f'{items}\n\nВсего: {len(var.list_del_values)}', icon='warning')
        if question:
            print(var.list_del_values)
            error_flag = False
            for item in var.list_del_values[::-1]:
                if not db.del_id(item[0]):
                    error_flag = True
            if not error_flag:
                mes.info('Удаление записей', 'Записи успешно удалены!')
            var.id_value = ''
            var.list_del_values.clear()
            reload()
        else:
            var.id_value = ''
            var.list_del_values.clear()
            print(var.list_del_values)
    else:
        question = messagebox.askokcancel(title='Удаление записи', message=f'Вы уверены, что хотите удалить запись '
                                                                           f'№{var.id_value} "{var.name_value}"?')
        if question:
            # print(var.id_value)
            if db.del_id(var.id_value):
                var.id_value = ''
            else:
                var.id_value = ''
            reload()


# Функции с вызовом действий с обновлением фрейма таблицы
def clear_db_and_reload():
    db.clear_db()
    var.back_to_sort = False
    reload()


def del_tab_and_reload():
    db.del_certs()
    var.back_to_sort = False
    reload()


def open_file_and_reload():
    add.open_file()
    var.back_to_sort = True
    reload()


def open_dir_and_reload():
    add.open_dir()
    var.back_to_sort = True
    reload()


# Запуск резервного копирования файлов БД
def start_backup():
    mes.info('Резервное копирование', 'Внимание!\nРезервное копирование будет проведено в два этапа в разные'
                                      ' расположения на сервере!')
    service.backup_bd('')
    service.backup_bd(var.path_all_backups_on_server)


# Запуск резервного восстановления файлов БД
def first_backup():
    service.write_backup_file(1)
    service.get_backup(root_closing, 1)


# Запуск резервного восстановления файлов БД
def get_backup():
    clear_frame()
    service.get_backup(root_closing, 0)
    show_table()


# показать таблицу, бинды действий, меню на пкм
def show_table():
    def check_id_value(event):
        id_value = var.id_value
        do_popup(event, id_value)

    def do_popup(event, id_value):
        var.back_to_sort = False
        if var.find_row != '' or var.temp_tag_value != '':
            m = Menu(root, tearoff=0)
            main_sort = Menu(m, tearoff=0)
            sort_menu = Menu(main_sort, tearoff=0)
            m.add_cascade(label="Сортировать", menu=sort_menu)
            sort_menu.add_command(label="ID", command=sort_search_id)
            sort_menu.add_command(label="ФИО", command=sort_search_name)
            sort_menu.add_command(label="Должность", command=sort_search_job)
            sort_menu.add_command(label="Серийный номер", command=sort_search_sn)
            sort_menu.add_command(label="Дата получения", command=sort_search_st)
            sort_menu.add_command(label="Дата окончания", command=sort_search_et)
            sort_menu.add_command(label="УЦ", command=sort_search_city)
            sort_menu.add_command(label="СНИЛС", command=sort_search_city)
            sort_menu.add_command(label="ИНН", command=sort_search_city)
            sort_menu.add_command(label="ОГРН", command=sort_search_city)
            sort_menu.add_command(label="Город", command=sort_search_city)
            sort_menu.add_command(label="Метка", command=sort_search_tag)
            sort_menu.add_command(label="Пройден инструктаж", command=sort_search_test)
            sort_menu.add_command(label="№ бланка тестирования", command=sort_search_blank_test)
            sort_menu.add_command(label="Дата тестирования", command=sort_search_test_data)

            m.add_separator()
            m.add_command(label="Копировать серийный номер", command=copy_cert)
            m.add_command(label="Копировать ФИО, должность, город", command=copy_cert_name_job_city)
            m.add_command(label="Копировать С№, ФИО, должность, город", command=copy_cert_serialnumber_name_job_city)
            m.add_command(label="Копировать данные ячейки", command=copy_cert_col)

            m.add_separator()
            m.add_command(label="Редактировать выбранную запись", command=edit_table)
            m.add_command(label="Удалить выбранные записи", command=delete_id)

            m.add_separator()
            m.add_command(label="Обновить", command=full_reload)

        elif id_value == '':
            # Контекстное меню на пкм
            m = Menu(root, tearoff=0)
            m.add_command(label="Найти заканчивающиеся сертификаты", command=show_date)
            m.add_separator()
            m.add_command(label="Добавить сертификат", command=open_file_and_reload)
            m.add_command(label="Добавить сертификаты из папки", command=open_dir_and_reload)
            m.add_separator()
            m.add_command(label="Удалить истекшие сертификаты", command=delete_old_certs)

            m.add_separator()
            main_sort = Menu(m, tearoff=0)
            sort_menu = Menu(main_sort, tearoff=0)
            m.add_cascade(label="Сортировать", menu=sort_menu)
            sort_menu.add_command(label="ID", command=sort_id)
            sort_menu.add_command(label="ФИО", command=sort_name)
            sort_menu.add_command(label="Серийный номер", command=sort_sn)
            sort_menu.add_command(label="Должность", command=sort_job)
            sort_menu.add_command(label="Дата получения", command=sort_st)
            sort_menu.add_command(label="Дата окончания", command=sort_et)
            sort_menu.add_command(label="Город", command=sort_city)
            sort_menu.add_command(label="Метка", command=sort_tag)
            sort_menu.add_command(label="Пройден инструктаж", command=sort_test)
            sort_menu.add_command(label="№ бланка тестирования", command=sort_blank_test)
            sort_menu.add_command(label="Дата тестирования", command=sort_test_data)

            m.add_separator()
            m.add_command(label="Обновить", command=full_reload)
        else:
            # Контекстное меню на лкм по записи и пкм
            m = Menu(root, tearoff=0)
            m.add_command(label="Найти заканчивающиеся сертификаты", command=show_date)
            m.add_separator()
            m.add_command(label="Добавить сертификат", command=open_file_and_reload)
            m.add_command(label="Добавить сертификаты из папки", command=open_dir_and_reload)
            m.add_separator()
            m.add_command(label="Удалить истекшие сертификаты", command=delete_old_certs)
            m.add_separator()
            m.add_command(label="Редактировать выбранную запись", command=edit_table)
            m.add_command(label="Удалить выбранные записи", command=delete_id)
            m.add_separator()
            main_sort = Menu(m, tearoff=0)
            sort_menu = Menu(main_sort, tearoff=0)
            m.add_cascade(label="Сортировать", menu=sort_menu)
            sort_menu.add_command(label="ID", command=sort_id)
            sort_menu.add_command(label="ФИО", command=sort_name)
            sort_menu.add_command(label="Серийный номер", command=sort_sn)
            sort_menu.add_command(label="Должность", command=sort_job)
            sort_menu.add_command(label="Дата получения", command=sort_st)
            sort_menu.add_command(label="Дата окончания", command=sort_et)
            sort_menu.add_command(label="Город", command=sort_city)
            sort_menu.add_command(label="Метка", command=sort_tag)
            sort_menu.add_command(label="Пройден инструктаж", command=sort_test)
            sort_menu.add_command(label="№ бланка тестирования", command=sort_blank_test)
            sort_menu.add_command(label="Дата тестирования", command=sort_test_data)
            m.add_separator()
            m.add_command(label="Копировать серийный номер", command=copy_cert)
            m.add_command(label="Копировать ФИО, должность, город", command=copy_cert_name_job_city)
            m.add_command(label="Копировать С№, ФИО, должность, город", command=copy_cert_serialnumber_name_job_city)
            m.add_command(label="Копировать данные ячейки", command=copy_cert_col)
            m.add_separator()
            m.add_command(label="Обновить", command=full_reload)

        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

    root.bind("<Button-3>", check_id_value)
    root.bind("<Double-Button-1>", edit_table_ev)

    # clear_frame()

    print(f'var.temp_sort = {var.temp_sort}', var.back_to_sort)
    if var.temp_sort != 0:
        clear_frame()
        # clear_tag_filter()
        sort = var.temp_sort
        if var.back_to_sort == True:
            if sort == 1 or sort == 2:
                sort_id()
                var.back_to_sort = False
            elif sort == 3 or sort == 4:
                sort_name()
                var.back_to_sort = False
            elif sort == 5 or sort == 6:
                sort_job()
                var.back_to_sort = False
            elif sort == 7 or sort == 8:
                sort_sn()
                var.back_to_sort = False
            elif sort == 9 or sort == 10:
                sort_st()
                var.back_to_sort = False
            elif sort == 11 or sort == 12:
                sort_et()
                var.back_to_sort = False
            elif sort == 13 or sort == 14:
                sort_uc()
                var.back_to_sort = False
            elif sort == 15 or sort == 16:
                sort_snils()
                var.back_to_sort = False
            elif sort == 17 or sort == 18:
                sort_inn()
                var.back_to_sort = False
            elif sort == 19 or sort == 20:
                sort_ogrn()
                var.back_to_sort = False
            elif sort == 21 or sort == 22:
                sort_city()
                var.back_to_sort = False
            elif sort == 23 or sort == 24:
                sort_tag()
                var.back_to_sort = False
            elif sort == 25 or sort == 26:
                sort_test()
                var.back_to_sort = False
            elif sort == 27 or sort == 28:
                sort_blank_test()
                var.back_to_sort = False
            elif sort == 29 or sort == 30:
                sort_test_data()
                var.sort_test_data = False
        else:
            clear_frame()
            if db.check_certs():
                data = ()
                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY id DESC")
                    data = (row for row in cursor.fetchall())
                    cursor.close()

                table = table_win.Table(f3, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                      'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                      'Дата Т', 'Примечание'), rows=data)
                table.pack(expand=tk.YES, fill=tk.BOTH)

                with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM certs ORDER BY id DESC")
                    results = cursor.fetchall()
                    cursor.close()

                label_count_of_certs['text'] = f'Всего записей: {len(results)}'
            else:
                mes.error('Вывод таблицы', 'Таблица не существует!')
    else:
        clear_frame()
        if db.check_certs():
            data = ()
            with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM certs ORDER BY id DESC")
                data = (row for row in cursor.fetchall())
                cursor.close()

            table = table_win.Table(f3, headings=('ID', 'ФИО', 'Должность', 'Номер', 'ОТ', 'ДО', 'УЦ', 'СНИЛС',
                                                  'ИНН', 'ОГРН', 'Город', 'Метка', 'Инстр-ж', '№ БТ',
                                                  'Дата Т', 'Примечание'), rows=data)
            table.pack(expand=tk.YES, fill=tk.BOTH)

            with sqlite3.connect(path_db + '/Certificates.sqlite') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM certs ORDER BY id DESC")
                results = cursor.fetchall()
                cursor.close()

            label_count_of_certs['text'] = f'Всего записей: {len(results)}'
        else:
            mes.error('Вывод таблицы', 'Таблица не существует!')


root = Tk()
root.title('Менеджер сертификатов')
root.geometry('1550x600+150+150')
root.resizable(True, True)
root.minsize(1150, 300)
root.protocol("WM_DELETE_WINDOW", root_closing)
s = ttk.Style()
s.theme_use('alt')

main_menu = Menu(root)
root.config(menu=main_menu, bg="#F1EEE9")

# Взаимодействие с таблицей
table_menu = Menu(main_menu, tearoff=0)
table_menu.add_command(label="Создать таблицу", command=db.create_db)
table_menu.add_command(label="Очистить таблицу", command=clear_db_and_reload)
table_menu.add_command(label="Удалить таблицу", command=del_tab_and_reload)
table_menu.add_command(label="Проверить существование таблицы", command=db.click_check_tab)
main_menu.add_cascade(label="Таблица", menu=table_menu)

# Добавление сертификатов
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="Добавить сертификат", command=open_file_and_reload)
file_menu.add_command(label="Добавить папку", command=open_dir_and_reload)
file_menu.add_separator()
file_menu.add_command(label="Удалить истекшие сертификаты", command=delete_old_certs)
main_menu.add_cascade(label="Сертификаты", menu=file_menu)

# Сервисное меню
service_menu = Menu(main_menu, tearoff=0)
service_menu.add_command(label="Провести резервное копирование БД на сервер", command=start_backup)
service_menu.add_command(label="Восстановить БД из резервной копии", command=first_backup)
main_menu.add_cascade(label="Сервис", menu=service_menu)

# О программе меню
about_menu = Menu(main_menu, tearoff=0)
about_menu.add_command(label="Открыть список изменений", command=service.open_changes)
about_menu.add_separator()
about_menu.add_command(label=f"Версия: {var.app_version} от {var.app_last_edit_version}", state='disabled')
about_menu.add_separator()
about_menu.add_command(label=f"Разработчик: Домашенко Иван Константинович. Администратор ИБ ВС, отдел ИТ", state='disabled')
main_menu.add_cascade(label="О программе", menu=about_menu)

f1 = Frame(root, bg="#F1EEE9")
f1.pack(fill=X, padx=10, pady=10)

f3 = Frame(root, bg='#73777B')
f3.pack(fill=BOTH, expand=True, padx=10, pady=10)

f4 = Frame(root, bg="#F1EEE9")
f4.pack(fill=X, padx=10)

label1 = Label(f1, text='Фильтр по метке: ', font="Helvetica 12", anchor=W, bg="#F1EEE9")
label1.pack(side=LEFT)

cb_filter_tag = ttk.Combobox(f1, font="Helvetica 9", postcommand=fill_cb_before_open)
cb_filter_tag['state'] = 'readonly'
cb_filter_tag.pack(padx=10, ipady=2, side=LEFT, fill=X)

cb_filter_tag.bind("<<ComboboxSelected>>", show_only_tag)

btn_clear_tag = Button(f1, font="Helvetica 9", bg="white", text='Сбросить', command=clear_tag_filter, padx=10,  pady=5)
btn_clear_tag.pack(side=LEFT)

btn_start_search = Button(f1, font="Helvetica 9", bg="white", text='Найти', command=start_search, padx=10, pady=5)
btn_start_search.pack(side=RIGHT)

e_search = Entry(f1, font="Helvetica 9", width=50, state=NORMAL)
e_search.pack(padx=10, ipady=2, side=RIGHT)

label2 = Label(f1, text='Поиск по ФИО | № | должности: ', font="Helvetica 12", anchor=W, bg="#F1EEE9")
label2.pack(side=RIGHT)

label_count_of_certs = Label(f4, font="Helvetica 9", anchor=W, bg="#F1EEE9")
label_count_of_certs.pack(side=LEFT)

label_version = Label(f4, font="Helvetica 9", text=f"ver.: {var.app_version} от {var.app_last_edit_version}", anchor=W, bg="#F1EEE9")
label_version.pack(side=RIGHT, padx=15)

status = service.check_backup_status()
if status == 'True':
    print(status)
    get_backup()

if db.check_certs():
    # обновляем таблицу при открытии программы
    reload()
    # Определяем ближайшие сроки окончания действия сертификатов (< 35 дней)
    check_near_info()
    # Открываем и закрываем второе окно чтобы избежать бага с недоступностью поля поиска
    edit_cert.edit_value(root, '', reload, True)

if var.exit_flag:
    exit()

root.mainloop()
