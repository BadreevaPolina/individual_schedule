from datetime import datetime
from datetime import timedelta
import json
from bs4 import BeautifulSoup
import requests


def add_json(day, date, times, place, data, name, errs, person):
    if day:
        data[name][day + ', ' + date] = []
        for i, time in enumerate(times):
            time, err = correct_time(time, date, name)
            if err != "":
                errs[person].append(err)
            one_str = {'time_begin': time[0], 'time_end': time[1], 'place': place[i]}
            data[name][day + ', ' + date].append(one_str)


def write_json_file(file, data):
    with open(file, "a", encoding="utf8") as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent=4)


def empty_file(file):
    with open(file, "w", encoding="utf8") as file:
        file.close()


def correct_time(times, date, name):
    time = times.split('\u2013')
    if len(time) == 2:
        return time, ""
    else:
        begin = datetime.strptime(time[0], "%H:%M")
        end = begin + timedelta(hours=1, minutes=35)
        return [begin.strftime('%H:%M'), end.strftime('%H:%M')], "На сайте timetable нет времени конца пары " + \
                                                                  date + " в " + begin.strftime('%H:%M') + " - " + \
                                                                  name + ". Предположено, что пара будет идти 1:35."


def find_info(soup, data, name, errs, person):
    panels = soup.findAll(class_='panel panel-default')
    for panel in panels:
        title = find_day(panel)
        times = find_time(panel)
        places = find_place(panel)
        if title is not None and times:
            day = title[0]
            date = title[1]
            add_json(day, date, times, places, data, name, errs, person)


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
    places = panel.findAll(True, {"class": ["col-sm-3 studyevent-locations",
                                            "col-sm-3 studyevent-multiple-locations"]})
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


def main_teacher(index, name):
    errs = {"student": [], "teacher": []}
    empty_file('static/json/teacher.json')
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    teacher_mas = {}
    teachers_index = index.split(',')
    for i, index in enumerate(teachers_index):
        if index != '' and index != ' ':
            teacher_mas[name[i]] = {}
            weeks = few_weeks()
            for week in weeks:
                url_teacher = 'https://timetable.spbu.ru/WeekEducatorEvents/' + index.strip() + '/' + str(week)
                url_teacher_ru = requests.get(url_teacher, cookies=cookie, timeout=10).text
                html_teacher = BeautifulSoup(url_teacher_ru, "lxml")
                find_info(html_teacher, teacher_mas, name[i], errs, "teacher")
    write_json_file('static/json/teacher.json', teacher_mas)
    try:
        with open('static/json/error.json', "r", encoding="utf8") as open_file:
            file_content = open_file.read()
            if not file_content:
                write_json_file('static/json/error.json', list(errs["teacher"]))
            else:
                data = json.loads(file_content)
                errs["student"] = data["student"]
                empty_file('static/json/error.json')
                write_json_file('static/json/error.json', list([list(errs["student"]), list(errs["teacher"])]))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def main_student(index, name):
    errs = {"student": [], "teacher": []}
    empty_file('static/json/student.json')
    empty_file('static/json/error.json')
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    student_mas = {}
    student_index = index.split(',')
    for i, index in enumerate(student_index):
        if index != '' and index != ' ':
            student_mas[name[i]] = {}
            weeks = few_weeks()
            for week in weeks:
                url_student = 'https://timetable.spbu.ru/MATH/StudentGroupEvents/Primary/' \
                              + index + '/' + str(week)
                url_student_ru = requests.get(url_student, cookies=cookie, timeout=10).text
                html_student = BeautifulSoup(url_student_ru, "lxml")
                find_info(html_student, student_mas, name[i], errs, "student")
    write_json_file('static/json/error.json', errs)
    write_json_file('static/json/student.json', student_mas)


if __name__ == '__main__':
    main_student("334764,334733,", "")
    main_teacher("2690, 12564, ", "")
