import variables as var
import certs_db as db
import get_messages as mes
import os
import pickle
from tkinter import messagebox


def fill_cb_from_file(data):
    tags = list()
    for item in var.tag_value_list:
        if item != '':
            print(f'data: {data}')
            if str(item) in data:
                data.remove(str(item))
            tags.append(str(item))
            for tag in data:
                temp_tag = str(tag).strip()
                temp_var_tag = str(item).strip()
                if temp_tag != temp_var_tag:
                    tags.append(tag)
                else:
                    continue
            var.tags_list_value.clear()
            var.tags_list_value = list(tuple(tags))
            var.tags_dict_value[str(item)] = str(item)
            tags_file_write(var.tags_dict_value)
        else:
            if str(item) in data:
                data.remove(str(item))
            tags.append(str(item))
            for tag in data:
                temp_tag = str(tag).strip()
                temp_var_tag = str(item).strip()
                if temp_tag != temp_var_tag:
                    tags.append(tag)
                else:
                    continue
            var.tags_list_value.clear()
            var.tags_list_value = list(tuple(tags))


# Работаем с байтовым файлом тэгов
def tag_file_wr():
    # Проверяем путь до папки с файлом
    if not db.check_path(var.path_listbox_byte_folder):
        db.create_path(var.path_listbox_byte_folder)
    # Проверяем наличие файла, если нет, заполняем базовыми тэгами
    if not os.path.exists(var.path_listbox_byte_file):
        dictionary = {'Электронная приемка': 'Электронная приемка',
                      'Начальство': 'Начальство',
                      '1С ЭДО ВН': '1С ЭДО ВН',
                      'Мед ЭДО': 'Мед ЭДО',
                      'Экономисты': 'Экономисты',
                      'Юристы': 'Юристы',
                      'Бухгалтерия': 'Бухгалтерия',
                      'Континент ЦИТ': 'Континент ЦИТ',
                      'Континент УФК': 'Континент УФК',
                      'Нет': 'Нет', }
        try:
            with open(var.path_listbox_byte_file, 'wb') as file:
                pickle.dump(dictionary, file, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            mes.error('Заполнение файла тэгов', f'Внимание!\nНе удалось создать и заполнить файл по шаблону!'
                                                f'\n\nПричина:\n{e}')
    temp_data_dict = {}
    temp_data_list = list()
    data = list()
    # Получаем тэги из файла
    with open(f'{var.path_listbox_byte_file}', 'rb') as file:
        while True:
            try:
                temp_data_dict = (pickle.load(file))
            except EOFError:
                break

    for key in temp_data_dict.keys():
        temp_data_list.append(key)
    print(temp_data_list)
    sorted_list = sorted(temp_data_list)
    print(f'\n\nsorted_list: {sorted_list}')
    var.tags_list_value = sorted_list
    for tag in var.tags_list_value:
        var.tags_dict_value[tag] = tag
    print(f'var.tags_dict_value: {var.tags_dict_value}')
    print(f'var.tags_list_value: {var.tags_list_value}')
    return sorted_list


def tags_file_write(dict):
    # Проверяем путь до папки с файлом
    if not db.check_path(var.path_listbox_byte_folder):
        db.create_path(var.path_listbox_byte_folder)
    # Перезаписывавем файл полученным словарем
    try:
        with open(var.path_listbox_byte_file, 'wb') as file:
            pickle.dump(dict, file, pickle.HIGHEST_PROTOCOL)
        print(f'Записал в файл словарь: {dict}')
    except Exception as e:
        mes.error('Заполнение файла тэгов', f'Внимание!\nНе удалось создать и заполнить файл полученными данными!'
                                            f'\n\nПричина:\n{e}')


# Добавление тэга
def add_tag(new_tag):
    try:
        # Добавляем в список
        var.tags_list_value.append(new_tag)
        # Добавляем в словарь
        var.tags_dict_value[new_tag] = new_tag
        # Перезаписываем файл по словарю
        tags_file_write(var.tags_dict_value)
        mes.info('Добавление новой метки', f'Успешно добавлена метка "{new_tag}"!')
    except Exception as e:
        mes.error('Добавление новой метки', f'Ошибка при создании метки:\n[{e}]!')


# Удаление тега
def del_tag(del_tag_temp):
    try:
        tag_for_delete = str(del_tag_temp)
        print(tag_for_delete, var.tag_value_for_send)
        print(type(tag_for_delete), type(var.tag_value_for_send))
        for item in var.tag_value_list:
            if tag_for_delete == str(item):
                mes.error('Удаление метки', f'Внимание!\nНе удается удалить метку "{tag_for_delete}", т.к. она относится к текущей записи!\n\nИзмените метку и сохраните запись для удаления.')
                return False
            else:
                question = messagebox.askokcancel(title='Удаление метки', message=f'Удалить метку {tag_for_delete} из списка?')
                if not question:
                    return False
                else:
                    # удаляем из списка
                    if tag_for_delete in var.tags_list_value:
                        var.tags_list_value.remove(tag_for_delete)
                    else:
                        mes.error('Удаление метки', 'Метка не находится в списке!')
                    # удаляем из словаря
                    if tag_for_delete in var.tags_dict_value:
                        del var.tags_dict_value[tag_for_delete]
                    # перезаписываем файл словарем
                    tags_file_write(var.tags_dict_value)
                    mes.info('Удаление метки', f'Метка "{tag_for_delete}" удалена.')
                    return True

    except Exception as e:
        mes.error('Удаление метки', f'Ошибка при удалении метки:\n[{e}]!')

