import os
import tkinter
from pathlib import Path
exit_flag = False
# Текущая версия программы
app_version = '1.7'
app_last_edit_version = '09.09.2023 г.'
# Путь для файла с изменениями
path_changes = os.path.abspath('Change_log.txt')

# переменная для форматирования выведенных на экран записей
data_values = ()

# Переменная для запоминания последнего открытого пути
last_path = ''

# Временные глобальные переменные
id_value = ''
name_value = ''
job_value = ''
sn_value = ''
start_value = ''
end_value = ''
uc_value = ''
snils_value = ''
inn_value = ''
ogrn_value = ''
tag_value_for_send = ''
tag_value_list = list()
briefing_value = ''
last_test_number_value = ''
last_test_date_value = ''
note_value = ''
city_value = ''

# Список для удаления нескольких записей
list_del_values = list()

# Переменная для копирования
temp_value = ''

# Переменные для сортировки
temp_sort = 0
back_to_sort = False

# Переменные для запоминания поиска
find_row = ''
need_find = False

# Переменная для сортировки в поиске
temp_search_sort = 0
back_to_search_sort = False

# Переменные для сортировки при выводе по тэгу
temp_tag_value = ''
temp_tag_sort_value = 0
back_to_tag_filter_sort = False
local_sort = False

# Переменная для состояния флажка инструктажа
briefing_var = 0

# Лист для выпадающего списка меток
tags_list_value = list()
tags_dict_value = {}

# Пути для конфига и БД
# path_default = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
path_db = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер сертификатов\База данных"
path_listbox_txt = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер сертификатов\База данных\config"
path_listbox_txt_file = os.path.join(path_listbox_txt, 'listbox_tag_data.txt')

path_listbox_byte_folder = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер сертификатов\База данных\config"
path_listbox_byte_file = os.path.join(path_listbox_byte_folder, 'listbox_tags_data.dat')

# Пути для резервного копирования
path_server_backup = r'\\192.168.15.4\Soft\Программирование\Py\Менеджер сертификатов\Резервная копия БД'
path_all_backups_on_server = r"\\192.168.15.4\Soft\Программирование\Py\Резервные копии\Менеджер сертификатов"

# Путь до документов пользователя
user_docs_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')

# Файл для операции резервного восстановления
path_start_backup_txt_folder = r"\\192.168.15.4\Soft\Программирование\Py\Менеджер сертификатов\База данных\config"
path_start_backup_txt_file = os.path.join(path_start_backup_txt_folder, 'backup_need_status.txt')
