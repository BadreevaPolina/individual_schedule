"""jsons with timetable information"""
from datetime import datetime
from datetime import timedelta
import json
from bs4 import BeautifulSoup
import requests


def add_json(day, date, times, place, subject, data, name, type_subject, incorrect_time_person):
    """string add in response array"""
    if day:
        data[name][day + ', ' + date] = []
        for i, time in enumerate(times):
            time, incorrect_time = correct_time(time, date, name)
            if incorrect_time != "":
                incorrect_time_person.append(incorrect_time)
            one_str = {'time_begin': time[0], 'time_end': time[1], 'place': place[i],
                       'subject': subject, 'type_subject': type_subject}
            data[name][day + ', ' + date].append(one_str)


def write_json_file(file, data):
    """add response array in file"""
    with open(file, "a", encoding="utf8") as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent=4)


def empty_file(file):
    """add response array in file"""
    with open(file, "w", encoding="utf8") as out_file:
        out_file.close()


def correct_time(times, date, name):
    """write correct time"""
    time = times.split('\u2013')
    if len(time) == 2:
        return time, ""
    begin = datetime.strptime(time[0], "%H:%M")
    end = begin + timedelta(hours=1, minutes=35)
    return [begin.strftime('%H:%M'), end.strftime('%H:%M')], "Не указано время конца пары " + \
            date + " в " + begin.strftime('%H:%M') + " - " + \
            name + ". Предполагается, что занятие будет длиться 1:35."


def find_subject(panel):
    subjects = panel.find_all('span', title='Предмет')
    if subjects is not None:
        for subject in subjects:
            print(subject)
            type_sub = subject.get_text().split(',')
            if len(type_sub) != 1:
                type_subject = type_sub[1]
                name_subject = type_sub[0]
            else:
                type_subject = type_sub
                name_subject = ""
            return name_subject.strip().replace("\r\n", ", "), type_subject.strip().replace("\r\n", "")
    return None, None


def find_info(soup, data, name, incorrect_time_person):
    """collect all information"""
    panels = soup.findAll(class_='panel panel-default')
    for panel in panels:
        title = find_day(panel)
        times = find_time(panel)
        places = find_place(panel)
        subjects, type_subjects = find_subject(panel)
        if title is not None and times:
            day = title[0]
            date = title[1]
            add_json(day, date, times, places, subjects, data, name, type_subjects, incorrect_time_person)


def find_day(panel):
    """information about day"""
    days = panel.find_all('h4', class_='panel-title')
    for day_str in days:
        only_day = day_str.get_text().split(',')
        day_param = only_day[0].strip()
        date_param = only_day[1].strip()
        title = [day_param.lower(), date_param.lower()]
        return title


def find_time(panel):
    """information about time"""
    times = panel.find_all('span', title='Время')
    time_array = []
    for time in times:
        time_param = time.get_text().strip()
        time_array.append(time_param)
    return time_array


def find_place(panel):
    """information about place"""
    places = panel.findAll(True, {"class": ["col-sm-3 studyevent-locations",
                                            "col-sm-3 studyevent-multiple-locations"]})
    place_array = []
    for place in places:
        street = place.get_text().split(',')
        place_param = street[0].strip()
        place_array.append(place_param)
    return place_array


def today_week():
    """define the start date of this week"""
    today = datetime.now().date()
    date = today - timedelta(datetime.now().weekday())
    return date


def few_weeks():
    """write the beginning of several weeks"""
    weeks = []
    this_week = today_week()
    for i in range(0, 4):
        date = this_week + timedelta(weeks=i)
        weeks.append(date)
    return weeks


def info_schedule(person_mas, name, url, incorrect_time_person):
    """info about schedule for several weeks"""
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    weeks = few_weeks()
    for week in weeks:
        url_person = url + str(week)
        url_person_ru = requests.get(url_person, cookies=cookie, timeout=10).text
        html_person = BeautifulSoup(url_person_ru, "lxml")
        find_info(html_person, person_mas, name, incorrect_time_person)
    return person_mas, incorrect_time_person


def write_incorrect_time(file, incorrect_time, person):
    """incorrect time in json file"""
    with open(file, encoding="utf8") as file_data:
        data = json.load(file_data)
    data[person] = incorrect_time[person]
    if incorrect_time[person] is not None:
        with open(file, "w", encoding="utf8") as out_file:
            json.dump(data, out_file, ensure_ascii=False, indent=4)


def main_teacher(input_index, name):
    """json with teachers timetable information"""
    incorrect_time = {"teacher": []}
    empty_file('static/json/teacher.json')
    teacher_mas = {}
    try:
        teachers_index = input_index.split(',')
        for i, index in enumerate(teachers_index):
            if index not in ('', ' '):
                url_teacher = 'https://timetable.spbu.ru/WeekEducatorEvents/' \
                              + index.strip() + '/'
                teacher_mas[name[i]] = {}
                teacher_mas, incorrect_time["teacher"] = info_schedule(teacher_mas,
                                                                       name[i], url_teacher,
                                                                       incorrect_time["teacher"])
        write_json_file('static/json/teacher.json', teacher_mas)
        write_incorrect_time('static/json/incorrect_data.json', incorrect_time, "teacher")
    except (AttributeError, IndexError, ConnectionError, FileNotFoundError, json.JSONDecodeError):
        pass


def main_student(input_index, name):
    """json with students timetable information"""
    incorrect_time = {"student": []}
    empty_file('static/json/student.json')
    empty_file('static/json/incorrect_data.json')
    write_json_file('static/json/incorrect_data.json', {"student": [], "teacher": []})
    student_mas = {}
    student_index = input_index.split(',')
    for i, index in enumerate(student_index):
        if index not in ('', ' '):
            url_student = 'https://timetable.spbu.ru/MATH/StudentGroupEvents/Primary/' \
                          + index + '/'
            student_mas[name[i]] = {}
            student_mas, incorrect_time["student"] = info_schedule(student_mas,
                                                                   name[i], url_student,
                                                                   incorrect_time["student"])
    write_incorrect_time('static/json/incorrect_data.json', incorrect_time, "student")
    write_json_file('static/json/student.json', student_mas)


if __name__ == '__main__':
    main_student("334764,334733,", ['1', '2'])  # example
    main_teacher("2690, 2167685, ", ['1', '2'])  # example
