import json
from datetime import datetime, timedelta

cookie = {
    "_culture": "ru",
    "value": "ru"
}

a = []
d = {"teacher": [], "student": []}
one_str = {}


def find_date(day):
    i = 0
    weekDays = ("понедельник", "вторник", "среда", "четверг", "пятница", "суббота")
    for i in range(len(weekDays)):
        if day == weekDays[i]:
            break
    today_date = datetime.now().date()
    date = today_date + timedelta(days=i - datetime.now().weekday())

    return str(date)


def add_json_free_time(day, begin, end, places, person):
    one_str = {'day': day, 'time_begin': end, 'place_begin': places[1],
               'time_end': begin, 'place_end': places[0]}
    d[person].append(one_str)


def add_json_answer(day, time_begin, time_end):
    date = find_date(day)
    date_title = datetime.strptime(date, "%Y-%m-%d").strftime("%m.%d.%Y")
    time_begin = date + "T" + time_begin + ":00.000"
    time_end = date + "T" + time_end + ":00.000"
    one_str = {'title': date_title, 'start': time_begin, 'end': time_end}
    a.append(one_str)


def write_json_file(file, tables):
    out_file = open(file, "w", encoding='utf-8')
    json.dump(tables, out_file, ensure_ascii=False, indent=4)
    out_file.close()


def free_time(file, person):
    f = open(file, encoding='utf-8')
    data = json.load(f)
    for day in data:
        end = "09:30"
        for i in data[day]:
            begin = i['time_begin']
            estimate_time(end, begin, day, person)  # end first lesson, begin second lesson
            end = i['time_end']
        estimate_time(end, "20:35", day, person)
    f.close()


def estimate_time(end, begin, day, person):
    e = datetime.strptime(end, "%H:%M")
    b = datetime.strptime(begin, "%H:%M")
    if b - e >= timedelta(hours=1, minutes=50):
        places = check_place(end, begin, day, person)
        if places[0] == places[1]:
            add_json_free_time(day, begin, end, places, person)
        else:
            if b - e >= timedelta(hours=3, minutes=50):
                add_json_free_time(day, begin, end, places, person)


def check_place(end, begin, day, person):
    place = ["", ""]
    if person == "teacher":
        f = open('static/json/teacher.json', encoding='utf-8')
    else:
        f = open('static/json/student.json', encoding='utf-8')
    data = json.load(f)
    for i in data[day]:
        if end == i['time_end']:
            place[0] = i['place']
        if begin == i['time_begin']:
            place[1] = i['place']
    if begin == "20:35":
        place[1] = place[0]
    if end == "09:30":
        place[0] = place[1]
    f.close()
    return place


def check_common_time(free):
    free_ = open(free, encoding='utf-8')
    d = json.load(free_)
    for i in d["teacher"]:
        day_check = False
        for j in d["student"]:
            if j['day'] == i['day']:
                day_check = True
                result_time = common_time(i['time_begin'], i['time_end'],
                                          j['time_begin'], j['time_end'])
                if result_time != "":
                    result_place = compare_place(result_time, i, j)
                    if result_place != "":
                        result_time = break_time(result_place[1])
                        add_json_answer(j['day'], result_time[0], result_time[1])
        if not day_check:
            result_time = common_time(i['time_begin'], i['time_end'],
                                      "09:30", "20:35")
            result_time = break_time(result_time)
            add_json_answer(i['day'], result_time[0], result_time[1])
    free_.close()


def common_time(b_t, e_t, b_s, e_s):  # begin_teacher....end_student
    t = datetime.strptime(b_t, "%H:%M")
    s = datetime.strptime(b_s, "%H:%M")
    begin_common_time = max(t, s)
    t = datetime.strptime(e_t, "%H:%M")
    s = datetime.strptime(e_s, "%H:%M")
    end_common_time = min(t, s)
    if end_common_time - begin_common_time >= timedelta(hours=1, minutes=50):
        res = begin_common_time.strftime('%H:%M') + "-" + end_common_time.strftime('%H:%M')
        return res
    return ""


def compare_place(result_time, i, j):  # проверить местоположение, успеет ли человек доехать
    result_time = result_time.split("-")
    b = datetime.strptime(result_time[0], "%H:%M")
    e = datetime.strptime(result_time[1], "%H:%M")
    res = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
    if i['place_begin'] == i['place_end']:
        if j['place_begin'] == j['place_end']:
            if i['place_begin'] == j['place_begin']:
                return [i['place_begin'], res]
            elif datetime.strptime(j['time_end'], "%H:%M") - datetime.strptime(j['time_begin'], "%H:%M") \
                        >= timedelta(hours=3, minutes=50):
                    result_time = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
                    return [i['place_begin'], result_time]
            elif i['place_end'] == j['place_end']:
                if datetime.strptime(j['time_end'], "%H:%M") - datetime.strptime(result_time[0], "%H:%M") \
                        >= timedelta(hours=3, minutes=50):
                    b = b + timedelta(hours=2, minutes=0)
                    result_time = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
                    return [i['place_end'], result_time]
            else:
                return ""
    else:
        if j['place_begin'] == j['place_end']:
            if i['place_begin'] == j['place_begin']:
                if datetime.strptime(i['time_end'], "%H:%M") - datetime.strptime(result_time[0], "%H:%M") \
                        >= timedelta(hours=3, minutes=50):
                    e = e - timedelta(hours=2, minutes=0)
                    result_time = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
                    return [j['place_begin'], result_time]
                else:
                    return ""
            elif i['place_end'] == j['place_end']:
                if datetime.strptime(j['time_end'], "%H:%M") - datetime.strptime(result_time[0], "%H:%M") \
                        >= timedelta(hours=3, minutes=50):
                    b = b + timedelta(hours=2, minutes=0)
                    result_time = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
                    return [j['place_end'], result_time]
                else:
                    return ""
            else:
                return ""
        else:
            if i['place_begin'] == j['place_begin'] and i['place_end'] == j['place_end']:
                if datetime.strptime(result_time[1], "%H:%M") - datetime.strptime(result_time[0], "%H:%M") \
                        >= timedelta(hours=3, minutes=50):
                    e = e - timedelta(hours=2, minutes=0)
                    result_time = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
                    return [j['place_begin'], result_time]
                else:
                    return ""
            elif i['place_begin'] == j['place_end'] and i['place_end'] == j['place_begin']:
                if datetime.strptime(result_time[1], "%H:%M") - datetime.strptime(result_time[0], "%H:%M") \
                        >= timedelta(hours=5, minutes=50):
                    e = e - timedelta(hours=2, minutes=0)
                    b = b + timedelta(hours=2, minutes=0)
                    result_time = b.strftime('%H:%M') + "-" + e.strftime('%H:%M')
                    return [j['place_begin'], result_time]
                else:
                    return ""
            else:
                return ""
    return ""


def break_time(result_time):
    res = ["", ""]
    result_time = result_time.split("-")
    b = datetime.strptime(result_time[0], "%H:%M")
    e = datetime.strptime(result_time[1], "%H:%M")
    if e - b >= timedelta(hours=1, minutes=50):
        if b == datetime.strptime("18:45", "%H:%M"):
            b = b + timedelta(hours=0, minutes=15)
        elif b == datetime.strptime("12:50", "%H:%M"):
            b = b + timedelta(hours=0, minutes=50)
        elif b == datetime.strptime("17:55", "%H:%M"):
            b = b + timedelta(hours=0, minutes=5)
        elif b == datetime.strptime("09:30", "%H:%M"):
            b = b + timedelta(hours=0, minutes=0)
        else:
            b = b + timedelta(hours=0, minutes=10)
        e = b + timedelta(hours=1, minutes=35)
        res[0] = b.strftime('%H:%M')
        res[1] = e.strftime('%H:%M')
        return res


if __name__ == '__main__':
    file_teacher = 'static/json/teacher.json'
    file_student = 'static/json/student.json'
    free = 'static/json/free_time.json'
    answer = 'static/json/answer.json'

    free_time(file_teacher, "teacher")
    free_time(file_student, "student")
    write_json_file(free, d)

    check_common_time(free)

    write_json_file(answer, a)
