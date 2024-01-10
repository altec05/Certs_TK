import errno
from distutils.dir_util import copy_tree
from variables import path_db, path_server_backup, path_start_backup_txt_file, path_start_backup_txt_folder
from certs_db import check_path
import get_messages as mes
import variables as var
import changes_list as chngs

import os
from check_funcs import empty_or_not, check_path
from pathlib import Path
import shutil
import sqlite3
import datetime
import time

from_directory = rf'{path_db}'
to_srv_directory = rf'{path_server_backup}'


def open_changes():
    # if check_path(var.path_changes):
    #     print(var.path_changes)
    #     os.system(fr"explorer.exe {var.path_changes}")
    # else:
        try:
            outp_file_path = var.path_changes.replace(os.path.basename(var.path_changes), '')
            file_path = outp_file_path + 'Change_log.txt'
            file = open(file_path, "w+")
            file.write(chngs.changes_row)
            file.close()

            if check_path(var.path_changes):
                print(var.path_changes)
                os.system(fr"explorer.exe {var.path_changes}")

        except Exception as e:
            mes.warning('Создание файла изменений', f'Не удалось записать файл изменений.\nПричина:\n[{e}]')


# Создать файл для начала резервного копирования
def write_backup_file(status):
    print(status)
    if check_path(path_start_backup_txt_file):
        os.remove(path_start_backup_txt_file)
        with open(path_start_backup_txt_file, 'w') as file:
            if status == 1:
                print('Записал True')
                file.write('True')
                file.close()
            else:
                print('Записал False')
                file.write('False')
                file.close()
    else:
        create_path(path_start_backup_txt_folder)
        with open(path_start_backup_txt_file, 'w') as file:
            if status == 1:
                print('Записал True')
                file.write('True')
                file.close()
            else:
                print('Записал False')
                file.write('False')
                file.close()


# Проверка необходимости резервного восстановления при запуске
def check_backup_status():
    print(f'Проверяю условие check_path(path_start_backup_txt_file) {check_path(path_start_backup_txt_file)}')
    if check_path(path_start_backup_txt_file):
        with open(path_start_backup_txt_file, 'r') as file:
            status = file.read()
            print(f'Прочитал статус {status}')
            file.close()
            print(f'Вернул статус {status}')
        os.remove(path_start_backup_txt_file)
        return status
    else:
        write_backup_file(0)
        with open(path_start_backup_txt_file, 'r') as file:
            status = file.read()
            print(f'Прочитал статус {status}')
            file.close()
            print(f'Вернул статус {status}')
        os.remove(path_start_backup_txt_file)
        return status


# Очистка временных переменных поиска и фильтрации
def clear_var_search_and_tag():
    var.find_row = ''
    var.need_find = False
    var.temp_search_sort = 0
    var.back_to_search_sort = False
    var.temp_tag_value = ''
    var.temp_tag_sort_value = 0
    var.back_to_tag_filter_sort = False
    var.local_sort = False
    print('Очистил поиск и фильтр')


# Перевод даты в корректную форму
def get_true_format(data):
    day = data[8:10]
    month = data[4:7]
    year = data[0:4]
    temp = day + month + '-' + year
    return temp


def create_path(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        mes.error('Создание пути', f'Ошибка создания пути!\n\nОшибка: [{e}]')


def clear_folder(path):
    import os, shutil
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f'Удалил {file_path}')
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f'Удалил {file_path}')
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def clear_old_backups(root, pass_path):
    paths = sorted(Path(root).iterdir(), key=os.path.getmtime)
    print(paths)
    print(pass_path)
    if len(paths) >= 2:
        for path in paths[:len(paths) - 2]:
            if str(path) == str(pass_path):
                print(f'Пропустили {path}')
                continue
            else:
                try:
                    print(f'Удаляем: {path}')
                    shutil.rmtree(path)
                except:
                    mes.warning('Удаление старой копии', f'При попытке удаления старой копии файлов'
                                                         f' произошла ошибка!\nУдаляли папку {path}')


# Резервное копирование по заданному пути
# на данном этапе изменение пути для РК не реализовано, но предусмотрено с необходимыми проверками
def backup_bd(extra_path):
    from datetime import datetime
    now_date = datetime.now().date().strftime("%d.%m.%Y")
    final_path = ''

    if extra_path == '':
        final_path = os.path.join(to_srv_directory, now_date)
    else:
        final_path = os.path.join(extra_path, now_date)
    root_dir = final_path.replace(now_date, '')
    try:
        if check_path(from_directory):
            if check_path(final_path):
                if empty_or_not(root_dir) is not None:
                    clear_old_backups(root_dir, final_path)
                if empty_or_not(final_path) is not None:
                    if mes.ask('Проверка пути для копирования',
                               f'Внимание! Конечная папка содержит файлы. Очистить её и продолжить копирование?\n\n{final_path}'):
                        clear_folder(final_path)
                        result = copy_tree(from_directory, final_path)
                        mes.info('Резервное копирование файлов',
                                 f'Успешно скопировано файлов: {len(result)}.\n\nСкопированы в: "{final_path}".')
                    else:
                        mes.error('Резервное копирование файлов', f'Отмена операции пользователем!')
                else:
                    result = copy_tree(from_directory, final_path)
                    mes.info('Резервное копирование файлов',
                             f'Успешно скопировано файлов: {len(result)}.\n\nСкопированы в: "{final_path}".')
            else:
                os.makedirs(final_path, exist_ok=True)
                result = copy_tree(from_directory, final_path)
                mes.info('Резервное копирование файлов',
                         f'Успешно скопировано файлов: {len(result)}.\n\nСкопированы в: "{final_path}".')
        else:
            mes.error('Резервное копирование файлов', f'Ошибка: путь с шаблонами не существует!\n\n{from_directory}')
    except OSError as exc:
        print(exc, exc.errno)
        # File already exist
        if exc.errno == errno.EEXIST:
            shutil.copy(from_directory, final_path)
        # The dirtory does not exist
        if exc.errno == errno.ENOENT:
            shutil.copy(from_directory, final_path)
        else:
            raise
    except Exception as e:
        mes.error('Резервное копирование БД', f'Ошибка: повторное копирование вызывает ошибку пути! Перезапустите программу и повторите попытку.\n\n----------\nОшибка:\n{e}')


# Восстановление файлов из последней резервной копии с сервера
def get_backup(root_func, status):
    # Куда копируем
    backup_to_path = from_directory
    # Папка с резервными копиями
    backup_root_dir = path_server_backup
    # Папка последней резервной копии
    backup_from_path = ''

    if check_path(backup_root_dir):
        if empty_or_not(backup_root_dir) is not None:
            paths = sorted(Path(backup_root_dir).iterdir(), key=os.path.getmtime)
            backup_from_path = str(paths[len(paths) - 1])
            print(backup_from_path)
            if not check_path(backup_to_path):
                os.makedirs(backup_to_path, exist_ok=True)
            if empty_or_not(backup_to_path) is not None:
                print(os.listdir(backup_to_path))
                if mes.ask('Проверка пути для копирования',
                           f'Внимание! Конечная папка содержит файлы. Очистить её и продолжить копирование?\n\n{backup_to_path}'):
                    print(f'Закрываем соединение!')
                    db = sqlite3.connect(path_db + '/Certificates.sqlite')
                    db.close()
                    with open(path_db + '/Certificates.sqlite', 'w+') as file:
                        file.close()
                    print(f'Закрыли соединение!')
                    print(f'Очищаем {backup_to_path}')
                    clear_folder(backup_to_path)
                    print(f'Копируем из {backup_from_path} в {backup_to_path}')
                    try:
                        result = copy_tree(backup_from_path, backup_to_path)
                        mes.info('Резервное копирование файлов',
                                 f'Успешно скопировано файлов: {len(result)}.\n\nСкопированы в: "{backup_to_path}".')
                    except Exception as e:
                        if str(e.__class__) == "<class 'distutils.errors.DistutilsFileError'>":
                            mes.error('Ошибка резервного копирования', 'Внимание!\n\nПри копировании не удалось получить'
                                                                       ' доступ к файлу БД для его замены.'
                                                                       '\n\nПерезапустите программу и сразу же '
                                                                       'попробуйте повторить копирование!')
                            if status == 1:
                                write_backup_file(1)
                            if root_func != '':
                                root_func()
                            else:
                                exit()
                        else:
                            mes.error('Ошибка резервного копирования',
                                      f'Внимание!\n\nПри копировании произошла непредвиденная ошибка!\n\nОшибка:\n{e}')
                else:
                    mes.error('Резервное копирование файлов', f'Отмена операции пользователем!')
            else:
                print(f'Копируем из {backup_from_path} в {backup_to_path}')
                try:
                    result = copy_tree(backup_from_path, backup_to_path)
                    mes.info('Резервное копирование файлов',
                             f'Успешно скопировано файлов: {len(result)}.\n\nСкопированы в: "{backup_to_path}".')
                except Exception as e:
                    if str(e.__class__) == "<class 'distutils.errors.DistutilsFileError'>":
                        mes.error('Ошибка резервного копирования', 'Внимание!\n\nПри копировании не удалось получить'
                                                                   ' доступ к файлу БД для его замены.'
                                                                   '\n\nПерезапустите программу и сразу же '
                                                                   'попробуйте повторить копирование!')
                        if status == 1:
                            write_backup_file(1)
                        if root_func != '':
                            root_func()
                        else:
                            exit()
                    else:
                        mes.error('Ошибка резервного копирования',
                                  f'Внимание!\n\nПри копировании произошла непредвиденная ошибка!\n\nОшибка:\n{e}')


def dif_timestamp(ts1, ts2):
    if ts1 > ts2:
        return True
    else:
        return False


def get_timestamp(date):
    timestamp = time.mktime(date.timetuple())
    return timestamp
