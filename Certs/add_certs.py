#-*-coding: UTF-8 -*-
import service
from certs_db import check_certs, check_path
import get_messages as mes
from variables import path_db, user_docs_path
import variables as var

from tkinter import filedialog, simpledialog
import os
import fsb795
import sqlite3
import datetime


# Получение файлов сертификатов из полученной папки
def find_certs(folder):
    tree = os.walk(folder, topdown=True, onerror=None, followlinks=False)
    certs = []
    for root, directories, files in os.walk(folder):
        for file in files:
            if not file.endswith('.cer'):
                continue
            else:
                if len(file) > 3:
                    certs.append(file)
                else:
                    continue
    return certs


# Получение реквизитов сертификата
def get_name(cert):
    cn = ''
    job = ''
    snils = ''
    inn = ''
    ogrn = ''
    sub, vlad_sub = cert.subjectCert()
    for key in sub.keys():

        if key == 'CN':
            cn = sub[key]
            try:
                print(f"cn.decode: {cn.encode().decode('utf-16-be')}")
                cn = cn.encode().decode('utf-16-be')
            except:
                print(cn)
            finally:
                print(f'CN: {cn}')
                if not str(cn)[0].lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz':
                    cn = sub[key]
        if key == 'title' or key == 'T':
            temp = sub[key]
            try:
                print(f"temp.decode: {temp.encode().decode('utf-16-be')}")
                temp = temp.encode().decode('utf-16-be')
            except:
                print(temp)
            finally:
                print(f'temp: {temp}')
            if temp == '':
                continue
            else:
                job = sub[key]
                try:
                    print(f"job.decode: {job.encode().decode('utf-16-be')}")
                    job = job.encode().decode('utf-16-be')
                except:
                    print(job)
                finally:
                    print(f'job: {job}')
                    if not str(job)[0].lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                        job = sub[key]
        if key == 'SNILS':
            snils = sub[key]
            try:
                print(f"snils.decode: {snils.encode().decode('utf-16-be')}")
                snils = snils.encode().decode('utf-16-be')
            except:
                print(snils)
            finally:
                print(f'snils: {snils}')
                if not str(snils)[0].lower() in '1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                    snils = sub[key]
        if key == 'INN':
            inn = sub[key]
            try:
                print(f"inn.decode: {inn.encode().decode('utf-16-be')}")
                inn = inn.encode().decode('utf-16-be')
            except:
                print(inn)
            finally:
                print(f'inn: {inn}')
                if not str(inn)[0].lower() in '1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                    inn = sub[key]
        if key == 'OGRN':
            ogrn = sub[key]
            try:
                print(f"ogrn.decode: {ogrn.encode().decode('utf-16-be')}")
                ogrn = ogrn.encode().decode('utf-16-be')
            except:
                print(ogrn)
            finally:
                print(f'ogrn: {ogrn}')
                if not str(ogrn)[0].lower() in '1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                    ogrn = sub[key]
    return cn, job, snils, inn, ogrn


# Получение даты сертификата
def get_date(cert):
    valid = cert.validityCert()
    start = valid["not_before"].date()
    end = valid["not_after"].date()
    print(f'start: {start}')
    print(f'end: {end}')
    return start, end


# Получение серийного номера сертификата
def get_sn(cert):
    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                        5: '5', 6: '6', 7: '7',
                        8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                        13: 'D', 14: 'E', 15: 'F'}

    def decimal_to_hexadecimal(decimal):
        hexadecimal = ''
        while (decimal > 0):
            remainder = decimal % 16
            hexadecimal = conversion_table[remainder] + hexadecimal
            decimal = decimal // 16

        return hexadecimal

    print(f'cert.serialNumber(): {cert.serialNumber()}')
    hex_output = decimal_to_hexadecimal(cert.serialNumber())
    print(f'hex_output: {hex_output}')
    return hex_output


# Получение удостоверяющего центра сертификата
def get_uc(cert):
    uc = ''
    iss, vlad_is = cert.issuerCert()
    for key in iss.keys():
        print(f'key uc: {key}')
        if key == 'CN':
            uc = iss[key]
            print(f"uc: {uc}")
            try:
                print(f"uc.decode: {uc.encode().decode('utf-16-be')}")
                return uc.encode().decode('utf-16-be')
            except:
                print(uc)
                return uc


# Получение города сертификата
def get_city(cert):
    city = ''
    sub, vlad_sub = cert.subjectCert()
    for key in sub.keys():
        if key == 'L':
            city = sub[key]
            try:
                city = city.encode().decode('utf-16-be')
            except Exception as e:
                # mes.error('Получение города сертификата', f'При получении сведений о городе произошла ошибка конвертации!\n\nОшибка:\n[{e}]')
                city = sub[key]
            if not city[0].lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                city = sub[key]
        if key == 'serialNumber':
            print(key, sub[key])
    print(f'city: {city}')
    return city


# Открытие файла сертификата
def open_file():
    if check_certs():
        filetypes = [("Сертификаты (*.cer) (*.cert) (*.CER)", "*.cer *.cert *.CER"), ("Все файлы", "*.*")]

        if var.last_path == '':
            get_path = filedialog.askopenfilename(title="Выбор файла сертификата",
                                                        initialdir=var.user_docs_path, filetypes=filetypes)
            if get_path != '':
                var.last_path = get_path.replace(os.path.basename(get_path), '')
                if check_certs():
                    get_serts(get_path)
                else:
                    mes.error('Добавление сертификата', 'Ошибка: Таблица не существует!')
        else:
            get_path = filedialog.askopenfilename(title="Выбор файла сертификата",
                                                        initialdir=var.last_path, filetypes=filetypes)
            if get_path != '':
                var.last_path = get_path.replace(os.path.basename(get_path), '')
                if check_certs():
                    get_serts(get_path)
                else:
                    mes.error('Добавление сертификата', 'Ошибка: Таблица не существует!')
    else:
        mes.error('Добавление сертификата', 'Ошибка: Таблица не существует!')


# Открытие сертификатов из папки
def open_dir():
    if check_certs():

        if var.last_path == '':
            get_path = filedialog.askdirectory()
            if get_path != '':
                var.last_path = get_path.replace(os.path.basename(get_path), '')
                if check_certs():
                    get_serts(get_path)
                else:
                    mes.error('Добавление сертификата', 'Ошибка: Таблица не существует!')
        else:
            get_path = filedialog.askdirectory()
            if get_path != '':
                var.last_path = get_path.replace(os.path.basename(get_path), '')
                if check_certs():
                    get_serts(get_path)
                else:
                    mes.error('Добавление сертификата', 'Ошибка: Таблица не существует!')
    else:
        mes.error('Добавление сертификатов из папки', 'Ошибка: Таблица не существует!')


# Проверка добавляемого сертификата в БД на корректность даты окончания
def check_date_end_correct(date_end):
    now = datetime.date.today()
    period = date_end - now
    if period.days < 0:
        return False
    else:
        return True


# Проверка добавляемого сертификата в БД на уникальность серийного номера
def check_uniq_cert(serial_number):
    need_find_list = []
    db1 = sqlite3.connect(path_db + '/Certificates.sqlite',
                          detect_types=sqlite3.PARSE_DECLTYPES |
                                       sqlite3.PARSE_COLNAMES)
    cursor = db1.cursor()
    serial_from_cert = str(serial_number).upper()
    need_find_list.append(serial_from_cert)
    need_find_list.append('00' + serial_from_cert)
    need_find_list.append('0' + serial_from_cert)

    finded_list = []
    for item in need_find_list:
        sql_search_query = f"""SELECT * FROM certs WHERE serial_number LIKE '%{item}%'"""
        print(sql_search_query)
        cursor.execute(sql_search_query)
        finded_rows = cursor.fetchall()
        if finded_rows:
            print('Нашел при добавлении строки:', finded_rows)
            finded_list.append(finded_rows)
    if len(finded_list) > 0:
        print('Найдены похожие строки:', finded_list)
        return False
    else:
        return True


# Получить записи из БД с таким же ФИО
def get_certs_from_bd_by_name(name):
    db1 = sqlite3.connect(path_db + '/Certificates.sqlite', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = db1.cursor()
    need_find = str(name).strip().title()
    sql_search_query = f"""SELECT * FROM certs WHERE name LIKE '%{need_find}%' ORDER BY id DESC"""
    cursor.execute(sql_search_query)
    finded_rows = cursor.fetchall()
    result = list()
    for row in finded_rows:
        result.append(row)
    db1.close()
    return result


# Сравниваем серийный номер, дату и ФИО и получаем метки
def get_tags_for_cert(items, name, sn, job, uc, data_start):
    send_data = []
    for item in items:
        if str(item[1]) == name:
            if str(item[3]) != str(sn):
                if str(item[2]) == job:
                    if str(item[6]) == uc:
                        true_date = service.get_timestamp(data_start)
                        checked_date = service.get_timestamp(item[4])
                        if service.dif_timestamp(true_date, checked_date):
                            send_data.append(item[11])
    if send_data:
        return send_data[0]
    else:
        return []


# Сравниваем серийный номер, дату и ФИО и получаем результаты инструктажа
def get_briefing_for_cert(items, name, sn, job, data_start):
    send_data = []
    for item in items:
        if str(item[1]) == name:
            if str(item[3]) != str(sn):
                if str(item[2]) == job:
                    true_date = service.get_timestamp(data_start)
                    checked_date = service.get_timestamp(item[4])
                    if service.dif_timestamp(true_date, checked_date):
                        send_data.append([item[12], item[13], item[14]])
    if send_data:
        return send_data[0]
    else:
        return []


# Разбор сертификата
def get_serts(get_path):
    skip_certs_sn_uniq = []
    skip_certs_date_stop = []
    path = get_path
    if path != '':
        if check_path(path):
            if not path.endswith('.cer'):
                folder_path = path
                certs = find_certs(folder_path)
                all_data = list()
                for cert in certs:
                    cert_name = cert
                    cert_path = folder_path + '\\' + cert_name

                    cert = fsb795.Certificate(cert_path)
                    # Получаем атрибуты сертификата в читаемом виде в списки
                    cert_data = get_name(cert)
                    cert_data_date = get_date(cert)
                    name = cert_data[0]
                    job = cert_data[1]
                    start = cert_data_date[0]
                    stop = cert_data_date[1]
                    if not check_date_end_correct(stop):
                        skip_certs_date_stop.append([name, stop])
                        continue
                    serial_number = ''
                    if get_sn(cert) != '':
                        serial_number = get_sn(cert).upper()
                    else:
                        USER_INP = simpledialog.askstring(title="Введите серийный номер",
                                                          prompt=f"Не удалось получить серийный номер для сертификата [{name} от {start.strftime('%d.%m.%Y')} до {stop.strftime('%d.%m.%Y')}].\n\nУкажите серийный номер вручную!")
                        print("Hello", USER_INP)
                        if USER_INP != '' and USER_INP is not None:
                            serial_number = USER_INP.upper()
                        else:
                            serial_number = '0'
                    if not check_uniq_cert(serial_number):
                        skip_certs_sn_uniq.append([name, serial_number])
                        continue
                    uc = get_uc(cert)
                    snils = str(cert_data[2])
                    inn = str(cert_data[3])
                    ogrn = str(cert_data[4])
                    city = str(get_city(cert))

                    tag_list = [
                        get_tags_for_cert(get_certs_from_bd_by_name(name), name, serial_number, job, uc, start)]

                    tag = 'Нет'
                    if tag_list[0]:
                        tag = tag_list[0]

                    brief_list = [
                        get_briefing_for_cert(get_certs_from_bd_by_name(name), name, serial_number, job, start)]

                    briefing = False
                    if brief_list[0]:
                        briefing = brief_list[0]
                    last_test_number = ''
                    if brief_list[1]:
                        last_test_number = service.get_true_format(brief_list[1])
                    last_test_date = ''
                    if brief_list[2]:
                        last_test_number = service.get_true_format(brief_list[2])
                    note = ''

                    data = (name, job, serial_number, start, stop, uc, inn, snils, ogrn, city, tag,
                            briefing, last_test_number, last_test_date, note)
                    all_data.append(data)

                db = sqlite3.connect(path_db + '/Certificates.sqlite')
                cursor = db.cursor()
                cursor.executemany(
                    "INSERT OR IGNORE INTO certs (name, job, serial_number, start_time, end_time, uc, inn, snils, "
                    "ogrn, city, tag, briefing, last_test_number, last_test_date, note) VALUES(?, ?, ?, ?, ?, ?, ?, "
                    "?, ?, ?, ?, ?, ?, ?, ?)",
                    all_data, )
                changes = db.total_changes

                db.commit()
                mes.info('Обработка сертификатов', f'Сертификаты успешно добавлены в таблицу!'
                                                   f' Было обработано {len(all_data)} '
                                                   f'сертификатов. Добавлено новых: {changes}')
                db.close()
                if len(skip_certs_sn_uniq) > 0:
                    temp = ''
                    counter = 1
                    for row in skip_certs_sn_uniq:
                        temp += str(counter) + '. '
                        for item in row:
                            temp += item + ', '
                        if temp.endswith(', '):
                            print(temp)
                            temp = temp[0:len(temp) - 2]
                            print(temp)
                        temp += '\n'
                        counter += 1
                    mes.warning('Пропущены сертификаты',
                                f'Внимание!\nСледующие сертификаты обработаны, но не добавлены,'
                                f' т.к. их серийные номера уже есть в базе данных!\nСертификатов: {len(skip_certs_sn_uniq)}\n\n{temp}')

                if len(skip_certs_date_stop) > 0:
                    temp = ''
                    counter = 1
                    for row in skip_certs_date_stop:
                        temp += str(counter) + '. '
                        for item in row:
                            if item.__class__ is datetime.date:
                                temp += str(service.get_true_format(str(item))) + ', '
                            else:
                                temp += item + ', '
                        if temp.endswith(', '):
                            print(temp)
                            temp = temp[0:len(temp) - 2]
                            print(temp)
                        temp += '\n'
                        counter += 1
                    mes.warning('Пропущены сертификаты',
                                f'Внимание!\nСледующие сертификаты обработаны, но не добавлены,'
                                f' т.к. их срок действия уже истек!\nСертификатов: {len(skip_certs_date_stop)}\n\n{temp}')
            else:
                all_data = list()

                cert = fsb795.Certificate(path)
                print(f'cert: {cert}')

                # Получаем атрибуты сертификата в читаемом виде в списки
                cert_data = get_name(cert)
                cert_data_date = get_date(cert)

                name = cert_data[0]
                job = cert_data[1]
                start = cert_data_date[0]
                stop = cert_data_date[1]
                serial_number = ''
                if get_sn(cert) != '':
                    serial_number = get_sn(cert).upper()
                else:
                    USER_INP = simpledialog.askstring(title="Введите серийный номер",
                                                      prompt=f"Не удалось получить серийный номер для сертификата [{name} от {start.strftime('%d.%m.%Y')} до {stop.strftime('%d.%m.%Y')}].\n\nУкажите серийный номер вручную!")
                    print("Hello", USER_INP)
                    if USER_INP != '' and USER_INP is not None:
                        serial_number = USER_INP.upper()
                    else:
                        serial_number = '0'
                if not check_uniq_cert(serial_number):
                    skip_certs_sn_uniq.append([name, serial_number])
                elif not check_date_end_correct(stop):
                    skip_certs_date_stop.append([name, stop])
                else:
                    uc = get_uc(cert)
                    snils = str(cert_data[2])
                    inn = str(cert_data[3])
                    ogrn = str(cert_data[4])
                    city = str(get_city(cert))

                    tag_list = [
                        get_tags_for_cert(get_certs_from_bd_by_name(name), name, serial_number, job, uc, start)]

                    tag = 'Нет'
                    if tag_list[0]:
                        tag = tag_list[0]

                    brief_list = get_briefing_for_cert(get_certs_from_bd_by_name(name), name, serial_number, job, start)

                    briefing = False
                    if brief_list:
                        briefing = brief_list[0]
                    last_test_number = ''
                    if brief_list:
                        last_test_number = brief_list[1]
                    last_test_date = ''
                    if brief_list:
                        last_test_date = datetime.datetime.strptime(service.get_true_format(str(brief_list[2])), "%d-%m-%Y").date()
                    note = ''

                    data = (name, job, serial_number, start, stop, uc, inn, snils, ogrn, city, tag,
                            briefing, last_test_number, last_test_date, note)
                    all_data.append(data)

                    db = sqlite3.connect(path_db + '/Certificates.sqlite')
                    cursor = db.cursor()

                    cursor.executemany(
                        "INSERT OR IGNORE INTO certs (name, job, serial_number, start_time, end_time, uc, inn, snils, "
                        "ogrn, city, tag, briefing, last_test_number, last_test_date, note) VALUES(?, ?, ?, ?, ?, ?, ?, "
                        "?, ?, ?, ?, ?, ?, ?, ?)",
                        all_data, )
                    changes = db.total_changes

                    db.commit()
                    if changes > 0:
                        mes.info("Обработка сертификатов", "Сертификат успешно добавлен в таблицу!")
                    else:
                        mes.warning("Обработка сертификатов",
                                    "Сертификат успешно обработан, но не добавлен т.к. уже зарегистрирован в таблице!")
                    db.close()
                if len(skip_certs_sn_uniq) > 0:
                    temp = ''
                    counter = 1
                    for row in skip_certs_sn_uniq:
                        temp += str(counter) + '. '
                        for item in row:
                            temp += item + ', '
                        if temp.endswith(', '):
                            print(temp)
                            temp = temp[0:len(temp) - 2]
                            print(temp)
                        temp += '\n'
                        counter += 1
                    mes.warning('Пропущены сертификаты',
                                f'Внимание!\nСледующие сертификаты обработаны, но не добавлены,'
                                f' т.к. их серийные номера уже есть в базе данных!\nСертификатов: {len(skip_certs_sn_uniq)}\n\n{temp}')
                if len(skip_certs_date_stop) > 0:
                    temp = ''
                    counter = 1
                    for row in skip_certs_date_stop:
                        temp += str(counter) + '. '
                        for item in row:
                            if item.__class__ is datetime.date:
                                temp += str(service.get_true_format(str(item))) + ', '
                            else:
                                temp += item + ', '
                        if temp.endswith(', '):
                            print(temp)
                            temp = temp[0:len(temp) - 2]
                            print(temp)
                        temp += '\n'
                        counter += 1
                    mes.warning('Пропущены сертификаты',
                                f'Внимание!\nСледующие сертификаты обработаны, но не добавлены,'
                                f' т.к. их срок действия уже истек!\nСертификатов: {len(skip_certs_date_stop)}\n\n{temp}')
            #   Предлагаем удалить сертификаты, которые уже были перевыпущены

        else:
            mes.error('Обработка сертификата', 'Ошибка: Запрашиваемый путь не найден!')
    else:
        mes.error('Обработка сертификата', 'Ошибка: Укажите путь к файлу!')
