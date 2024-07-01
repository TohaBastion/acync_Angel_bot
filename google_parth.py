"""Файл для API запитів Google Sheets"""

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime
import os

credentials = os.getenv("GOOGLE_CREDS")


def google_request(table_name):
    """Основна функція запитів Google Sheets"""
    link = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    my_credentials = ServiceAccountCredentials.from_json_keyfile_name(f'{credentials}', link)

    client = gspread.authorize(my_credentials)
    sheet = client.open(table_name).sheet1

    get_data = sheet.get_all_records()
    return get_data


def google_parth_schedule(table_name):
    """Пошук та виокремлення даниз щодо майбутніх ігор команди"""
    schedule_list = []
    data = google_request(table_name)
    target_team = 'Ангели'
    today = datetime.datetime.today().date()
    for row in data:
        if ((row['first_team'] == target_team or row['second_team'] == target_team) and
                (datetime.datetime.strptime(row['date'], '%d.%m.%Y').date()) >= today):
            date = row['date']
            first_team = row['first_team']
            second_team = row['second_team']
            schedule_list.append(f'{date}:  {first_team} - {second_team}')
    return schedule_list


def google_parth_schedule_pull(table_name):
    """Пошук та виокремлення ігор які повинні відбутися через n днів, задля формування
    опитування присутності на грі"""
    schedule_list = []
    data = google_request(table_name)
    target_team = 'Ангели'
    today = datetime.datetime.today().date()
    time_delta = datetime.timedelta(days=4)
    date_x = today + time_delta
    for row in data:
        if ((row['first_team'] == target_team or row['second_team'] == target_team) and
                (datetime.datetime.strptime(row['date'], '%d.%m.%Y').date()) == date_x):
            schedule_list.append(row)
    print(schedule_list)
    return schedule_list


def google_parth_birthday(table_name):
    """Перевірка чи є сьогодні в когось День Народження і якщо так, то формування поздоровлення."""
    birthday_list = []
    data = google_request(table_name)
    today = datetime.datetime.today().date()
    for row in data:
        birthday = (datetime.datetime.strptime(row['birthday'], '%d.%m.%Y').date())
        if (birthday.day == today.day) and (birthday.month == today.month):
            first_name = row['first_name']
            last_name = row['last_name']
            birthday_list.append(f'Сьогодні святкує День Народження наш\nвельмишановний {first_name} {last_name}!\n '
                                 f'Чіназес!')
    return birthday_list
