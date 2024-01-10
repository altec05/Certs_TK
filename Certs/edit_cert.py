import locale
import os.path
from tkinter import *
from tkinter import ttk
import sqlite3
import re
import datetime

import tags_win
from variables import path_db
import get_messages as mes
import get_messages as ms
import variables as var
import service

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def edit_value(root, data, root_func, exit=False):
    # проверка наличия обязательных полей
    def check_entry():
        if e_name.get() != '' and e_job.get() != '' and e_sn.get() != '' and box_of_tags.size() > 0:
            return True
        else:
            return False

    # проверка формата даты
    def check_data(type_of_date):
        def check_len_and_place1(data, sep, clear):
            place1 = [2, 5]
            if [_.start() for _ in re.finditer(sep, data)] == place1:
                if len(clear) == 8:
                    return True
                else:
                    return False
            else:
                return False

        def check_len_and_place2(data, sep, clear):
            place2 = [4, 7]
            if [m.start() for m in re.finditer(sep.strip(), data)] == place2:
                if len(clear) == 8:
                    return True
                else:
                    return False
            else:
                return False

        def check_date_1():
            if e_last_test_date.get() != '':
                no_clear = e_last_test_date.get()
                clear_dot = no_clear.replace('.', '')
                digit = ''.join([i for i in no_clear if i.isdigit()])
                if '-' in no_clear and '.' in no_clear:
                    return False
                # 1 дд.мм.гггг
                elif '.' in no_clear and not '-' in no_clear:
                    if clear_dot.isdigit() and check_len_and_place1(no_clear, '\.', digit):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        def check_date_2():
            if e_last_test_date.get() != '':
                no_clear = e_last_test_date.get()
                clear_minus = no_clear.replace('-', '')
                digit = ''.join([i for i in no_clear if i.isdigit()])
                if '-' in no_clear and '.' in no_clear:
                    return False
                # 2 дд-мм-гггг
                elif '-' in no_clear and not '.' in no_clear:
                    if clear_minus.isdigit() and check_len_and_place1(no_clear, '-', digit):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        def check_date_3():
            if e_last_test_date.get() != '':
                no_clear = e_last_test_date.get()
                clear_minus = no_clear.replace('-', '')
                digit = ''.join([i for i in no_clear if i.isdigit()])
                if '-' in no_clear and '.' in no_clear:
                    return False
                # 3 гггг-мм-дд
                elif '-' in no_clear and not '.' in no_clear:
                    if clear_minus.isdigit() and check_len_and_place2(no_clear, '-', digit):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        if type_of_date == 1:
            if check_date_1():
                return True
        elif type_of_date == 2:
            if check_date_2():
                return True
        elif type_of_date == 3:
            if check_date_3():
                return True
        elif type_of_date == 0:
            if e_last_test_date.get() != '':
                if check_date_1() or check_date_2() or check_date_3():
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    # очистка глобальных временных переменных
    def clear_var():
        var.id_value = ''
        var.name_value = ''
        var.job_value = ''
        var.sn_value = ''
        var.briefing_value = ''
        var.last_test_number_value = ''
        var.last_test_date_value = ''
        var.note_value = ''
        var.tags_list_value.clear()
        var.tag_value_for_send = ''
        var.tag_value_list.clear()

    # очистка полей ввода после отправки записи
    def clear_entry():
        e_name.delete(0, END)
        e_job.delete(0, END)
        e_sn.delete(0, END)
        box_of_tags.delete(0, box_of_tags.size())
        rb_briefing.delete(0, END)
        e_last_test_number.delete(0, END)
        e_last_test_date.delete(0, END)
        e_note.delete(0, END)

    # заполнение полей ввода при открытии редактирования записи
    def fill_entry():
        clear_entry()
        e_name.insert(0, data[1])
        e_job.insert(0, data[2])
        e_sn.insert(0, data[3])
        fill_box_of_tags()
        # fill_cb_before_open()
        if var.briefing_value == 1:
            rb_briefing.current(0)
        else:
            rb_briefing.current(1)
        e_last_test_number.insert(0, data[6])
        if data[7] != '' and data[7] != 'None':
            e_last_test_date.insert(0, datetime.datetime.strptime(service.get_true_format(data[7]), "%d-%m-%Y").strftime("%d-%m-%Y"))
        else:
            e_last_test_date.insert(0, data[7])
        e_note.insert(0, data[8])

    # Проверка полей инструктажа по результату выбора в выпадающем списке
    def check_rb_briefing():
        if rb_briefing.get() == 'Да':
            if e_last_test_date.get() != '' and e_last_test_number.get() != '':
                return True
            else:
                return False
        else:
            return True

    # считать данные из полей ввода
    def get_data():
        name = e_name.get()
        job = e_job.get()
        sn = e_sn.get()
        tags_from_box = list(box_of_tags.get(0, box_of_tags.size()))
        tags_from_box.sort()
        delim = ', '
        tags = delim.join(map(str, tags_from_box))
        if rb_briefing.get() == 'Да':
            briefing = 1
        else:
            briefing = 0
        if briefing == 1 and str(e_last_test_number.get()) == '':
            mes.error('Проверка данных', 'Если указан инструктаж, то необходимо указать номер бланка тестирования!')
            return False
        else:
            if e_last_test_number.get().isdigit():
                last_test_number = int(e_last_test_number.get())
            else:
                last_test_number = e_last_test_number.get()

            send_last_test_date = ''
            if e_last_test_date.get() != '':
                if check_data(1):
                    # 1
                    date1 = e_last_test_date.get().rsplit(sep='.')
                    date1_normal = date1[0] + '-' + date1[1] + '-' + date1[2]

                    last_test_date = datetime.datetime.strptime(date1_normal, "%d-%m-%Y")
                    send_last_test_date = last_test_date.date()
                elif check_data(2):
                    # 2
                    date2 = e_last_test_date.get().rsplit(sep='-')
                    date2_normal = date2[0] + '-' + date2[1] + '-' + date2[2]

                    last_test_date = datetime.datetime.strptime(date2_normal, "%d-%m-%Y")
                    send_last_test_date = last_test_date.date()
                elif check_data(3):
                    # 3
                    date3 = e_last_test_date.get().rsplit(sep='-')
                    date3_normal = date3[0] + '-' + date3[1] + '-' + date3[2]

                    last_test_date = datetime.datetime.strptime(date3_normal, "%d-%m-%Y")
                    send_last_test_date = last_test_date.date()

            note = e_note.get()
            send_data = (name, job, sn.upper(), tags, briefing, last_test_number, send_last_test_date, note)
            return send_data

    # отправить введенные данные
    def confirm():
        if check_data(0):
            if check_entry():
                if check_rb_briefing():
                    # try:
                    id_value = data[0]
                    send_data = get_data()
                    if send_data != False:
                        db = sqlite3.connect(path_db + '/Certificates.sqlite')
                        cursor = db.cursor()
                        sql_update_query = """UPDATE certs SET name = ?, job = ?, serial_number = ?, tag = ?, 
                                                    briefing = ?, last_test_number = ?, last_test_date = ?, note = ? WHERE id = ?"""
                        query_data = (send_data[0], send_data[1], send_data[2], send_data[3], send_data[4], send_data[5],
                                      send_data[6], send_data[7], id_value)
                        cursor.execute(sql_update_query, query_data)
                        cursor.close()
                        db.commit()
                        db.close()
                        mes.info("Обработка сертификата",
                                 "Сертификат успешно обновлен!\nДля отображения изменений обновите таблицу.")
                        clear_var()
                        edit_cert_closing()
                else:
                    mes.error('Проверка данных', 'Ошибка: вы указали прохождение инструктажа, но не указали данные '
                                                 'тестирования!')
            else:
                ms.error('Валидация значений', 'Ошибка: обязательные поля не заполнены!')
        else:
            ms.error('Валидация значений', 'Ошибка формата даты!\nИспользуйте формат дд.мм.гггг')

    # закрытие окна и разворачивание главного окна без обновления таблицы
    def edit_cert_closing_no_reload():
        print('Закрыт без обновления')
        clear_var()
        var.id_value = ''
        var.back_to_sort = True
        if var.find_row != '':
            var.need_find = True
            var.back_to_search_sort = True
        elif var.temp_tag_value != '':
            var.back_to_tag_filter_sort = True
        else:
            var.need_find = False
            var.back_to_tag_filter_sort = False
        edit.destroy()
        root.deiconify()

    # закрытие окна и разворачивание главного окна с обновлением таблицы
    def edit_cert_closing():
        print('Закрыт с обновлением')
        clear_var()
        var.id_value = ''
        var.back_to_sort = True
        if var.find_row != '':
            var.need_find = True
            var.back_to_search_sort = True
        elif var.temp_tag_value != '':
            var.back_to_tag_filter_sort = True
        else:
            var.need_find = False
            var.back_to_tag_filter_sort = False
        edit.destroy()
        # if not exit != True:
        if not var.exit_flag:
            root.deiconify()
        root_func()

    # Заполнение списка меток по сертификату
    def fill_box_of_tags():
        box_of_tags.delete(0, box_of_tags.size())
        print('var.tag_value_list:', var.tag_value_list)
        for item in var.tag_value_list[::-1]:
            box_of_tags.insert(0, item)

    # Переход к окну выбора меток
    def edit_tags():
        tags_win.show_tags_win(edit, edit_cert_closing, var.tag_value_list, fill_box_of_tags)

    edit = Toplevel()
    edit.title('Редактор сертификата')
    edit.geometry('600x650+300+200')
    edit.resizable(True, False)
    edit.minsize(600, 300)
    edit.protocol("WM_DELETE_WINDOW", edit_cert_closing_no_reload)

    main_menu = Menu(edit)
    edit.config(menu=main_menu)

    f1 = Frame(edit)
    f1.pack(fill=X, padx=10, pady=10)

    f2 = Frame(edit)
    f2.pack(fill=X, padx=10, pady=10)

    f3 = Frame(edit)
    f3.pack(fill=X, padx=10, pady=10)

    f4 = Frame(edit)
    f4.pack(fill=X, padx=10, pady=10)

    f4_1 = Frame(edit)
    f4_1.pack(fill=X, padx=10, pady=10)

    f4_2 = Frame(edit)
    f4_2.pack(fill=X, padx=10, pady=10)

    f5 = Frame(edit)
    f5.pack(fill=X, padx=10, pady=10)

    f6 = Frame(edit)
    f6.pack(fill=X, padx=10, pady=10)

    f7 = Frame(edit)
    f7.pack(fill=X, padx=10, pady=10)

    f8 = Frame(edit)
    f8.pack(fill=X, padx=10, pady=10)

    f9 = Frame(edit)
    f9.pack(fill=X, padx=10, pady=10)

    label1 = Label(f1, text='* ФИО: ', font="Helvetica 12", width=25, anchor=W)
    label1.pack(side=LEFT)

    e_name = Entry(f1, font="Helvetica 9")
    e_name.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label2 = Label(f2, text='* Должность: ', font="Helvetica 12", width=25, anchor=W)
    label2.pack(side=LEFT)

    e_job = Entry(f2, font="Helvetica 9")
    e_job.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label2 = Label(f3, text='* Серийный номер: ', font="Helvetica 12", width=25, anchor=W)
    label2.pack(side=LEFT)

    e_sn = Entry(f3, font="Helvetica 9")
    e_sn.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label3 = Label(f4, text='* Метки: ', font="Helvetica 12", width=25, anchor=W)
    label3.pack(side=LEFT)

    box_of_tags = Listbox(f4, selectmode=SINGLE)
    box_of_tags.pack(side=LEFT)

    scroll = Scrollbar(f4, command=box_of_tags.yview)
    scroll.pack(side=LEFT)

    box_of_tags.config(yscrollcommand=scroll.set)

    btn_edit_tags = Button(f4, font="Helvetica 9", bg="#fca311", text='Выбрать метки', command=edit_tags, padx=10, pady=5)
    btn_edit_tags.pack(side=RIGHT)

    label4 = Label(f5, text='Инструктаж: ', font="Helvetica 12", width=25, anchor=W)
    label4.pack(side=LEFT)

    rb_briefing = ttk.Combobox(f5, font="Helvetica 9", values=['Да', 'Нет'])
    rb_briefing['state'] = 'readonly'
    rb_briefing.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label5 = Label(f6, text='Номер посл-го тестирования: ', font="Helvetica 12", width=25, anchor=W)
    label5.pack(side=LEFT)

    e_last_test_number = Entry(f6, font="Helvetica 9")
    e_last_test_number.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label6 = Label(f7, text='Дата посл-го тестирования: ', font="Helvetica 12", width=25, anchor=W)
    label6.pack(side=LEFT)

    e_last_test_date = Entry(f7, font="Helvetica 9")
    e_last_test_date.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    label7 = Label(f8, text='Примечание: ', font="Helvetica 12", width=25, anchor=W)
    label7.pack(side=LEFT)

    e_note = Entry(f8, font="Helvetica 9")
    e_note.pack(padx=10, ipady=2, side=LEFT, expand=True, fill=X)

    btn_confirm = Button(f9, font="Helvetica 9", bg="#fca311", text='Принять', command=confirm, padx=10, pady=5)
    btn_confirm.pack(side=RIGHT)

    # заполняем поля при открытии формы
    if data != '':
        fill_entry()
    if exit == True:
        edit_cert_closing()
