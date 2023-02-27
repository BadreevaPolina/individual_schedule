import json
from datetime import datetime, timedelta


def date_week(day_month):
    year = datetime.now().year
    date = str(year) + '-'
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августa', 'сентября', 'октября', 'ноября',
              'декабря']
    for i in range(len(months)):
        if months[i] == day_month.split(' ')[1]:
            date = date + str(i + 1) + '-' + str(day_month.split(' ')[0])
            date = datetime.strptime(date, "%Y-%m-%d")
            break
    return str(date)


def add_json_free_time(day, begin, end, places, person, d):
    one_str = {'day': day.split(', ')[0], 'day_month': day.split(', ')[1], 'time_begin': end, 'place_begin': places[0],
               'time_end': begin, 'place_end': places[1]}
    d[person].append(one_str)


def format_time(time, date_title):
    time_format = datetime.strptime(time, "%H:%M")
    time_change = date_title + timedelta(hours=time_format.hour, minutes=time_format.minute)
    time_str = time_change.strftime("%Y-%m-%dT%H:%M:%S")
    return time_str


def add_json_answer(day_month, time_begin, time_end, a, color):
    date = date_week(day_month)
    date_title = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    title = date_title.strftime("%d.%m.%Y")
    time_begin_str = format_time(time_begin, date_title)
    time_end_str = format_time(time_end, date_title)
    if color == "#cc6d33":
        one_str = {'title': "Занятие у студента", 'start': time_begin_str, 'end': time_end_str, 'color': color}
    elif color == "#3f4bc0":
        one_str = {'title': "Занятие у преподавателя", 'start': time_begin_str, 'end': time_end_str, 'color': color}
    else:
        one_str = {'title': title, 'start': time_begin_str, 'end': time_end_str, 'color': color}
    a.append(one_str)


def write_json_file(file, tables):
    out_file = open(file, "w", encoding='utf-8')
    json.dump(tables, out_file, ensure_ascii=False, indent=4)
    out_file.close()


def free_time(file, person, d, flag):
    f = open(file, encoding='utf-8')
    data = json.load(f)
    for day in data:
        end = "09:30"
        for i in data[day]:
            begin = i['time_begin']
            estimate_time(end, begin, day, person, d, flag)  # end first lesson, begin second lesson
            end = i['time_end']
        estimate_time(end, "20:35", day, person, d, flag)
    f.close()


def estimate_time(end, begin, day, person, d, flag):
    e = datetime.strptime(end, "%H:%M")
    b = datetime.strptime(begin, "%H:%M")
    if b - e >= timedelta(hours=1, minutes=45):
        if flag == "True":
            places = ["", ""]
            add_json_free_time(day, begin, end, places, person, d)
        else:
            places = check_place(end, begin, day, person)
            if places[0] == places[1]:
                add_json_free_time(day, begin, end, places, person, d)
            else:
                if b - e >= timedelta(hours=3, minutes=45):
                    add_json_free_time(day, begin, end, places, person, d)


def check_place(end, begin, day, person):  # end first lesson, begin second lesson
    place = ["", ""]
    if person == "teacher":
        f = open('static/json/teacher.json', encoding='utf-8')
    else:
        f = open('static/json/student.json', encoding='utf-8')
    read = json.load(f)
    for i in read[day]:
        if end == i['time_end']:
            place[0] = i['place']
        if begin == i['time_begin']:
            place[1] = i['place']
    if begin == "20:35":
        place[1] = "Университетский проспект"
    if end == "09:30":
        place[0] = "Университетский проспект"
    f.close()
    return place


def check_common_time(free, a, flag):
    color = "#4e8bb1"
    free_ = open(free, encoding='utf-8')
    read = json.load(free_)
    for i in read["teacher"]:
        day_check = False
        for j in read["student"]:
            if j['day_month'] == i['day_month']:
                day_check = True
                result_time = common_time(i['time_begin'], i['time_end'],
                                          j['time_begin'], j['time_end'])
                if result_time != "":
                    if flag == "False":
                        new_place, new_time = compare_place(result_time, i, j)
                        if new_time != "":
                            time_begin, time_end = break_time(new_time)
                            add_json_answer(i['day_month'], time_begin, time_end, a, color)
                    else:
                        time_begin, time_end = break_time(result_time)
                        add_json_answer(i['day_month'], time_begin, time_end, a, color)
        if not day_check:
            result_time = common_time(i['time_begin'], i['time_end'],
                                      "09:30", "20:35")
            time_begin, time_end = break_time(result_time)
            add_json_answer(i['day_month'], time_begin, time_end, a, color)
    free_.close()


def common_time(b_t, e_t, b_s, e_s):  # begin_teacher....end_student
    t = datetime.strptime(b_t, "%H:%M")
    s = datetime.strptime(b_s, "%H:%M")
    begin_common_time = max(t, s)
    t = datetime.strptime(e_t, "%H:%M")
    s = datetime.strptime(e_s, "%H:%M")
    end_common_time = min(t, s)
    if end_common_time - begin_common_time >= timedelta(hours=1, minutes=45):
        res = begin_common_time.strftime('%H:%M') + "-" + end_common_time.strftime('%H:%M')
        return res
    return ""


def compare_place(result_time, i, j):  # teacher - i, student - j
    result_time = result_time.split("-")
    b = datetime.strptime(result_time[0], "%H:%M")
    e = datetime.strptime(result_time[1], "%H:%M")
    res = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
    if i['place_begin'] == i['place_end']:
        if j['place_begin'] == j['place_end']:
            if i['place_begin'] == j['place_begin']:
                return i['place_begin'], res
            elif datetime.strptime(j['time_end'], "%H:%M") - datetime.strptime(j['time_begin'], "%H:%M") \
                    >= timedelta(hours=5, minutes=45):
                b = b + timedelta(hours=2, minutes=0)
                e = e - timedelta(hours=2, minutes=0)
                result_time = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
                return i['place_begin'], result_time
            else:
                return "", ""
        else:
            return begin_or_end_equals(result_time, i, j)
    else:
        if j['place_begin'] == j['place_end']:
            return begin_or_end_equals(result_time, j, i)
        return ""


def begin_or_end_equals(result_time, i, j):
    b = datetime.strptime(result_time[0], "%H:%M")
    e = datetime.strptime(result_time[1], "%H:%M")
    res = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
    if i['place_begin'] == j['place_begin']:
        if datetime.strptime(j['time_end'], "%H:%M") - datetime.strptime(result_time[0], "%H:%M") \
                >= timedelta(hours=3, minutes=45):
            return i['place_begin'], res
        else:
            return "", ""
    elif i['place_end'] == j['place_end']:
        if datetime.strptime(result_time[1], "%H:%M") - datetime.strptime(j['time_begin'], "%H:%M") \
                >= timedelta(hours=3, minutes=45):
            return i['place_end'], res
        else:
            return "", ""
    else:
        return "", ""


def change_begin_time(b):
    if b == datetime.strptime("09:30", "%H:%M"):
        b = b + timedelta(hours=0, minutes=0)
    elif b == datetime.strptime("12:50", "%H:%M"):
        b = b + timedelta(hours=0, minutes=50)
    elif b == datetime.strptime("17:55", "%H:%M"):
        b = b + timedelta(hours=0, minutes=5)
    elif b == datetime.strptime("18:45", "%H:%M"):
        b = b + timedelta(hours=0, minutes=15)
    else:
        b = b + timedelta(hours=0, minutes=10)
    return b


def change_end_time(e):
    if e == datetime.strptime("11:15", "%H:%M"):
        e = e - timedelta(hours=0, minutes=10)
    elif e == datetime.strptime("13:40", "%H:%M"):
        e = e - timedelta(hours=0, minutes=50)
    elif e == datetime.strptime("15:25", "%H:%M"):
        e = e - timedelta(hours=0, minutes=10)
    elif e == datetime.strptime("17:10", "%H:%M"):
        e = e - timedelta(hours=0, minutes=10)
    elif e == datetime.strptime("20:35", "%H:%M"):
        e = e - timedelta(hours=0, minutes=0)
    else:
        e = e - timedelta(hours=0, minutes=5)
    return e


def break_time(result_time):
    res = ["", ""]
    result_time = result_time.split("-")
    b = datetime.strptime(result_time[0], "%H:%M")
    e = datetime.strptime(result_time[1], "%H:%M")
    res[0] = change_begin_time(b).strftime('%H:%M')
    res[1] = change_end_time(e).strftime('%H:%M')
    return res


def add_in_answer(file, a, color):
    f = open(file, encoding='utf-8')
    read = json.load(f)
    for i in read:
        for j in read[i]:
            add_json_answer(i.split(', ')[1], j['time_begin'], j['time_end'], a, color)


def check_answer_empty(a, file_teacher, file_student):
    if not a:
        add_in_answer(file_student, a, color="#cc6d33")
        add_in_answer(file_teacher, a, color="#3f4bc0")


def main(flag):
    file_teacher = 'static/json/teacher.json'
    file_student = 'static/json/student.json'
    free = 'static/json/free_time.json'
    answer = 'static/json/answer.json'

    free_time_mas = {"teacher": [], "student": []}
    free_time(file_teacher, "teacher", free_time_mas, flag)
    free_time(file_student, "student", free_time_mas, flag)
    write_json_file(free, free_time_mas)
    answer_mas = []
    check_common_time(free, answer_mas, flag)
    check_answer_empty(answer_mas, file_teacher, file_student)
    write_json_file(answer, answer_mas)


if __name__ == '__main__':
    main("False")
