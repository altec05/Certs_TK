from tkinter import *

import get_messages as mes
import variables as var
import tags


def show_tags_win(root_win, root_func, cert_tags, box_of_tags_update):
    def tags_win_closing():
        tags_win.destroy()
        root_win.deiconify()
        box_of_tags_update()

    def save_tags():
        to_tags = list(box_to.get(0, box_to.size()))
        var.tag_value_list.clear()
        for t_tag in to_tags:
            if t_tag in var.tag_value_list:
                continue
            else:
                var.tag_value_list.append(t_tag)
        print('Отправил метки:', var.tag_value_list)
        tags_win_closing()

    # Заполнение списка меток
    def fill_all_tags_list_before_open():
        box_from.delete(0, box_from.size())
        tags.fill_cb_from_file(tags.tag_file_wr(), )
        for item in var.tags_list_value[::-1]:
            to_tags = list(box_to.get(0, box_to.size()))
            need_insert = True
            for t_tag in to_tags:
                if item == t_tag:
                    need_insert = False
                    break
                else:
                    continue
            from_tags = list(box_from.get(0, box_from.size()))
            for f_tag in from_tags:
                if item == f_tag:
                    need_insert = False
                    break
            if need_insert:
                box_from.insert(0, item)
            else:
                continue

    # Заполнение списка выбранных меток
    def fill_cert_tags_before_open():
        if cert_tags:
            box_to.delete(0, box_to.size())
            from_tags = list(box_from.get(0, box_from.size()))
            for tag in cert_tags:
                if tag in from_tags:
                    counter = 0
                    for check_tag in from_tags:
                        if tag == check_tag:
                            print('tag', tag, 'check_tag', check_tag, counter)
                            box_from.delete(counter)
                            if box_to.size() > 0:
                                to_tags = list(box_to.get(0, box_to.size()))
                                need_insert = True
                                for t_tag in to_tags:
                                    if tag == t_tag:
                                        need_insert = False
                                        break
                                    else:
                                        continue
                                if need_insert:
                                    box_to.insert(0, tag)
                            else:
                                box_to.insert(0, tag)
                            break
                        else:
                            counter += 1
                            continue
                else:
                    box_to.insert(0, tag)

    # Добавление метки из списка существующих в список выбранных
    def get_tag_to_to():
        if box_from.curselection():
            select = list(box_from.curselection())
            for item in select:
                box_to.insert(0, box_from.get(item))
                box_from.delete(item)

    # Добавление метки из списка выбранных в список существующих
    def get_tag_to_from():
        if box_to.curselection():
            select = list(box_to.curselection())
            for item in select:
                box_from.insert(0, box_to.get(item))
                box_to.delete(item)

    # Удаление метки из списка
    def del_tag():
        del_tag_value = ''
        del_tag_id = ''
        if box_from.curselection():
            del_tag_value = box_from.get(box_from.curselection())
            del_tag_id = box_from.curselection()
        elif box_to.curselection():
            del_tag_value = box_to.get(box_to.curselection())
            del_tag_id = box_to.curselection()
        if del_tag_value != '':
            if tags.del_tag(str(del_tag_value)):
                to_tags = list(box_to.get(0, box_to.size()))
                for t_tag in to_tags:
                    if str(del_tag_value) == t_tag:
                        box_to.delete(del_tag_id)
                box_from.select_clear(0, box_from.size())
                box_to.select_clear(0, box_to.size())
                fill_all_tags_list_before_open()
                # fill_cert_tags_before_open()

    # Добавление нового тега с проверкой
    def add_tag():
        if e_new_tag.get().strip() != '':
            if not e_new_tag.get().strip() in var.tags_list_value:
                new_tag = str(e_new_tag.get().strip())
                tags.add_tag(new_tag)
                e_new_tag.delete(0, END)
                fill_all_tags_list_before_open()
                fill_cert_tags_before_open()
            else:
                mes.error('Добавление новой метки', 'Ошибка: указанная метка уже существует!')
        else:
            mes.error('Добавление новой метки', 'Ошибка: введите значение!')

    tags_win = Toplevel()
    tags_win.title('Метки для сертификата')
    tags_win.geometry('800x150+300+200')
    tags_win.resizable(False, False)
    tags_win.minsize(800, 150)
    tags_win.protocol("WM_DELETE_WINDOW", tags_win_closing)

    f1 = Frame(tags_win)
    f1.pack(padx=10, pady=10, side=LEFT, anchor=N)

    f2 = Frame(tags_win)
    f2.pack(padx=10, pady=10, side=LEFT, anchor=N)

    f3 = Frame(tags_win)
    f3.pack(padx=10, pady=10, side=LEFT, anchor=N)

    f4 = Frame(tags_win)
    f4.pack(padx=10, pady=10, side=LEFT, anchor=W)

    box_from = Listbox(f1, selectmode=SINGLE)
    box_from.pack(side=LEFT)

    scroll = Scrollbar(f1, command=box_from.yview)
    scroll.pack(side=RIGHT, fill=Y)

    box_from.config(yscrollcommand=scroll.set)

    btn_get_tag = Button(f2, text=">>>", font="Helvetica 9", command=get_tag_to_to)
    btn_get_tag.pack()

    btn_del_tag = Button(f2, text="<<<", font="Helvetica 9", command=get_tag_to_from)
    btn_del_tag.pack()

    btn_full_del_tag = Button(f2, text="Удалить", font="Helvetica 9", command=del_tag)
    btn_full_del_tag.pack()

    btn_confirm_tags = Button(f2, text="Сохранить", font="Helvetica 9", bg="#fca311", command=save_tags)
    btn_confirm_tags.pack()

    box_to = Listbox(f3, selectmode=SINGLE)
    box_to.pack(side=LEFT)

    scroll = Scrollbar(f3, command=box_to.yview)
    scroll.pack(side=RIGHT, fill=Y)

    box_to.config(yscrollcommand=scroll.set)

    e_new_tag = Entry(f4, width=30)
    e_new_tag.pack(side=LEFT, fill=X, padx=10)

    btn_add_new_tag = Button(f4, text="Добавить новый тэг", font="Helvetica 9", command=add_tag)
    btn_add_new_tag.pack(side=LEFT, ipadx=3, ipady=3, padx=10)

    tags_win.grab_set()

    fill_cert_tags_before_open()
    fill_all_tags_list_before_open()

    