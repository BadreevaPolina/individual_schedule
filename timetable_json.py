from datetime import datetime
from datetime import timedelta
import json
from bs4 import BeautifulSoup
import requests


def add_json(day, date, time, place, data):
    if day:
        data[day + ', ' + date] = []
        for i in range(len(place)):
            time[i] = time[i].split('\u2013')
            one_str = {'time_begin': time[i][0], 'time_end': time[i][1], 'place': place[i]}
            data[day + ', ' + date].append(one_str)


def write_json_file(file, data):
    out_file = open(file, "a", encoding='utf8')
    json.dump(data, out_file, ensure_ascii=False, indent=4)
    out_file.close()


def empty_file(file):
    out_file = open(file, "w", encoding='utf8')
    out_file.close()


def find_info(soup, data):
    panels = soup.findAll(class_='panel panel-default')
    for panel in panels:
        title = find_day(panel)
        if title is not None:
            d = title[0]
            date = title[1]
            ts = find_time(panel)
            ps = find_place(panel)
            add_json(d, date, ts, ps, data)


def find_day(panel):
    days = panel.find_all('h4', class_='panel-title')
    for day_str in days:
        only_day = day_str.get_text().split(',')
        day_param = only_day[0].strip()
        date_param = only_day[1].strip()
        title = [day_param.lower(), date_param.lower()]
        return title


def find_time(panel):
    times = panel.find_all('span', title='Время')
    time_array = []
    for time in times:
        time_param = time.get_text().strip()
        time_array.append(time_param)
    return time_array


def find_place(panel):
    places = panel.findAll(True, {"class": ["col-sm-3 studyevent-locations", "col-sm-3 studyevent-multiple-locations"]})
    place_array = []
    for place in places:
        street = place.get_text().split(',')
        place_param = street[0].strip()
        place_array.append(place_param)
    return place_array


def today_week():
    today = datetime.now().date()
    date = today - timedelta(datetime.now().weekday())
    return date


def few_weeks():
    weeks = []
    this_week = today_week()
    for i in range(0, 4):
        date = this_week + timedelta(weeks=i)
        weeks.append(date)
    return weeks


def main_teacher(index):
    empty_file('static/json/teacher.json')
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    t = {}
    weeks = few_weeks()
    for week in weeks:
        url_teacher = 'https://timetable.spbu.ru/WeekEducatorEvents/' + index + '/' + str(week)
        url_teacher_ru = requests.get(url_teacher, cookies=cookie).text
        html_teacher = BeautifulSoup(url_teacher_ru, "lxml")
        find_info(html_teacher, t)
    write_json_file('static/json/teacher.json', t)


def main_student(index):
    empty_file('static/json/student.json')
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    s = {}
    weeks = few_weeks()
    for week in weeks:
        url_student = 'https://timetable.spbu.ru/MATH/StudentGroupEvents/Primary/' + index + '/' + str(week)
        url_student_ru = requests.get(url_student, cookies=cookie).text
        html_student = BeautifulSoup(url_student_ru, "lxml")
        find_info(html_student, s)
    write_json_file('static/json/student.json', s)

