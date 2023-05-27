"""define result"""
import json
from datetime import datetime, timedelta


def date_week(day_month):
    """find date in begin week for answer"""
    year = datetime.now().year
    date = str(year) + '-'
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
              'августa', 'сентября', 'октября', 'ноября', 'декабря']
    for i, month in enumerate(months):
        if month == day_month.split(' ')[1]:
            date = date + str(i + 1) + '-' + str(day_month.split(' ')[0])
            date = datetime.strptime(date, "%Y-%m-%d")
            break
    return str(date)


def add_json_free_time(day, begin, end, places, free_time_mas):
    """string add in free time file"""
    one_str = {'day': day.split(', ')[0], 'day_month': day.split(', ')[1],
               'time_begin': end, 'place_begin': places[0],
               'time_end': begin, 'place_end': places[1]}
    free_time_mas.append(one_str)


def format_time(time, date_title):
    """make a standard response time"""
    time_format = datetime.strptime(time, "%H:%M")
    time_change = date_title + timedelta(hours=time_format.hour, minutes=time_format.minute)
    time_str = time_change.strftime("%Y-%m-%dT%H:%M:%S")
    return time_str


def add_json_answer(day_month, time_begin, time_end, answer_mas, color, title):
    """string add in response array"""
    date = date_week(day_month)
    date_title = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    if title == "":
        title = date_title.strftime("%d.%m.%Y")
    time_begin_str = format_time(time_begin, date_title)
    time_end_str = format_time(time_end, date_title)
    one_str = {'title': title, 'start': time_begin_str,
               'end': time_end_str, 'color': color}
    answer_mas.append(one_str)


def write_json_file(file, tables):
    """add response array in file"""
    with open(file, "w", encoding="utf8") as out_file:
        json.dump(tables, out_file, ensure_ascii=False, indent=4)


def free_time(file, person, free_time_mas, flag):
    """free time for person"""
    with open(file, encoding="utf8") as open_file:
        data = json.load(open_file)
        for num in data:
            free_time_mas[person][num] = []
            for day in data[num]:
                end = "09:30"
                for i in data[num][day]:
                    begin = i['time_begin']
                    # end first lesson, begin second lesson
                    estimate_time(end, begin, day, person, num, free_time_mas, flag)
                    end = i['time_end']
                estimate_time(end, "20:40", day, person, num, free_time_mas, flag)


def estimate_time(end_time, begin_time, day, person, num, free_time_mas, flag):
    """check if the time is fits"""
    end = datetime.strptime(end_time, "%H:%M")
    begin = datetime.strptime(begin_time, "%H:%M")
    if begin - end >= timedelta(hours=1, minutes=45):
        if flag == "True":
            places = ["", ""]
            add_json_free_time(day, begin_time, end_time, places,
                               free_time_mas[person][num])
        else:
            places = check_place(end_time, begin_time, day, person, num)
            if places[0] == places[1]:
                add_json_free_time(day, begin_time, end_time,
                                   places, free_time_mas[person][num])
            else:
                if begin - end >= timedelta(hours=3, minutes=45):
                    add_json_free_time(day, begin_time, end_time,
                                       places, free_time_mas[person][num])


def check_place(end, begin, day, person, num):  # end first lesson, begin second lesson
    """check location match"""
    place = ["", ""]
    if person == "teacher":
        with open('static/json/teacher.json', encoding="utf8") as file:
            read = json.load(file)
    else:
        with open('static/json/student.json', encoding="utf8") as file:
            read = json.load(file)
    for i in read[num][day]:
        if end == i['time_end']:
            place[0] = i['place']
        if begin == i['time_begin']:
            place[1] = i['place']
    if begin == "20:40":
        place[1] = "Университетский проспект"
    if end == "09:30":
        place[0] = "Университетский проспект"
    return place


def change_json_free_time(day, time_begin, time_end, place, free_time_mas):
    """change free time array """
    one_str = {'day_month': day,
               'time_begin': time_begin, 'place_begin': place,
               'time_end': time_end, 'place_end': place}
    free_time_mas.append(one_str)


def check_common_time_persons(free_time_mas, flag):
    """check common time teacher(student) and teacher(student)"""
    for _, person_i in enumerate(free_time_mas):
        keys = free_time_mas[person_i].keys()
        key_mas = []
        for k in keys:
            key_mas.append(k)
        for p in range(len(key_mas) - 1):
            person1_mas = free_time_mas[person_i][key_mas[p]]
            person2_mas = free_time_mas[person_i][key_mas[p + 1]]

            free_time_mas[person_i].pop(key_mas[p])
            free_time_mas[person_i].pop(key_mas[p + 1])

            free_time_mas[person_i][key_mas[p + 1]] = []
            for person1 in person1_mas:
                for person2 in person2_mas:
                    if person1['day_month'] == person2['day_month']:
                        result_time = common_time(person1['time_begin'], person1['time_end'],
                                                  person2['time_begin'], person2['time_end'])
                        if result_time != "":
                            if flag == "False":
                                new_place, new_time = compare_place(result_time, person1, person2)
                                if new_time != "" and new_place != "":
                                    time_begin, time_end = new_time.split("-")
                                    change_json_free_time(person1['day_month'], time_begin,
                                                          time_end, new_place,
                                                          free_time_mas[person_i][key_mas[p + 1]])
                            else:
                                time_begin, time_end = result_time.split("-")
                                change_json_free_time(person1['day_month'], time_begin, time_end,
                                                      person1['place_begin'],
                                                      free_time_mas[person_i][key_mas[p + 1]])


def free_time_in_answer(free_time_mas, answer_mas):
    """make response a free time file"""
    color_mas = ["#71AB7E", "#ffcc99", "#E3DD95", "#6D6D6e", "#F1B7B3",
                 "#B8A8CC", "#99ccff", "#73d978", "#ccff66"]
    color_number = 0
    count = len(free_time_mas['student']) + len(free_time_mas['teacher'])
    for i in free_time_mas:
        color_number += 1
        for j in free_time_mas[i]:
            for k in free_time_mas[i][j]:
                if count == 1:
                    color = "#4e8bb1"
                else:
                    color = color_mas[color_number % 9]
                add_json_answer(k['day_month'], k['time_begin'],
                                k['time_end'], answer_mas, color, "")


def break_time_in_mas(free_time_mas):
    """change break time"""
    for i in free_time_mas:
        for k in free_time_mas[i]:
            for j in free_time_mas[i][k]:
                j["time_begin"], j["time_end"] = break_time(j["time_begin"] + "-" + j["time_end"])


def find_common_time(free, free_time_mas, answer_mas, flag):
    """find common time depending on the situation"""
    with open(free, encoding="utf8") as file:
        read = json.load(file)
    if len(read["teacher"]) == len(read["student"]) == 1:
        check_common_time_s_t(free, answer_mas, flag, True)
    elif (len(read["teacher"]) > 0 and len(read["student"]) == 0) or \
            (len(read["student"]) > 0 and len(read["teacher"]) == 0):
        check_common_time_persons(free_time_mas, flag)
        break_time_in_mas(free_time_mas)
        write_json_file(free, free_time_mas)
        free_time_in_answer(free_time_mas, answer_mas)
    elif len(read["teacher"]) > 0 and len(read["student"]) > 0:
        check_common_time_persons(free_time_mas, flag)
        write_json_file(free, free_time_mas)
        check_common_time_s_t(free, answer_mas, flag, False)


def check_common_time_s_t(free, answer_mas, flag, with_day_check):
    """check common time student and teacher"""
    color = "#4e8bb1"
    with open(free, encoding="utf8") as file:
        read = json.load(file)
    for k1 in read["teacher"]:
        for i in read["teacher"][k1]:
            day_check = False
            for k2 in read["student"]:
                for j in read["student"][k2]:
                    if j['day_month'] == i['day_month']:
                        day_check = True
                        result_time = common_time(i['time_begin'], i['time_end'],
                                                  j['time_begin'], j['time_end'])
                        if result_time != "":
                            if flag == "False":
                                new_place, new_time = compare_place(result_time, i, j)
                                if new_time != "" and new_place != "":
                                    time_begin, time_end = break_time(new_time)
                                    add_json_answer(i['day_month'], time_begin, time_end,
                                                    answer_mas, color, "")
                            else:
                                time_begin, time_end = break_time(result_time)
                                add_json_answer(i['day_month'], time_begin, time_end,
                                                answer_mas, color, "")
            if not day_check and with_day_check:
                result_time = common_time(i['time_begin'], i['time_end'],
                                          "09:30", "20:40")
                time_begin, time_end = break_time(result_time)
                add_json_answer(i['day_month'], time_begin, time_end, answer_mas, color, "")


def common_time(b_t, e_t, b_s, e_s):  # begin_teacher....end_student
    """find common time between two people"""
    teacher = datetime.strptime(b_t, "%H:%M")
    student = datetime.strptime(b_s, "%H:%M")
    begin_common_time = max(teacher, student)
    teacher = datetime.strptime(e_t, "%H:%M")
    student = datetime.strptime(e_s, "%H:%M")
    end_common_time = min(teacher, student)
    if end_common_time - begin_common_time >= timedelta(hours=1, minutes=45):
        res = begin_common_time.strftime('%H:%M') + "-" + end_common_time.strftime('%H:%M')
        return res
    return ""


def compare_place(result_time, i, j):  # teacher - i, student - j
    """ compare place between two people"""
    result_time = result_time.split("-")
    begin = datetime.strptime(result_time[0], "%H:%M")
    end = datetime.strptime(result_time[1], "%H:%M")
    res = begin.strftime('%H:%M') + "-" + end.strftime('%H:%M')
    if i['place_begin'] == i['place_end']:
        if j['place_begin'] == j['place_end']:
            if i['place_begin'] == j['place_begin']:
                return i['place_begin'], res
            if datetime.strptime(j['time_end'], "%H:%M") - \
                    datetime.strptime(j['time_begin'], "%H:%M") >= timedelta(hours=5, minutes=45):
                begin = begin + timedelta(hours=2, minutes=0)
                end = end - timedelta(hours=2, minutes=0)
                result_time = begin.strftime('%H:%M') + "-" + end.strftime('%H:%M')
                return i['place_begin'], result_time
            return "", ""
        return begin_or_end_equals(result_time, i, j)
    if j['place_begin'] == j['place_end']:
        return begin_or_end_equals(result_time, j, i)
    return "", ""


def begin_or_end_equals(result_time, i, j):
    """compare place between two people"""
    begin = datetime.strptime(result_time[0], "%H:%M")
    end = datetime.strptime(result_time[1], "%H:%M")
    res = begin.strftime('%H:%M') + "-" + end.strftime('%H:%M')
    if i['place_begin'] == j['place_begin']:
        if datetime.strptime(j['time_end'], "%H:%M") \
                - datetime.strptime(result_time[0], "%H:%M") \
                >= timedelta(hours=3, minutes=45):
            return i['place_begin'], res
        return "", ""
    if i['place_end'] == j['place_end']:
        if datetime.strptime(result_time[1], "%H:%M") \
                - datetime.strptime(j['time_begin'], "%H:%M") \
                >= timedelta(hours=3, minutes=45):
            return i['place_end'], res
        return "", ""
    return "", ""


def change_begin_time(begin):
    """add change"""
    if begin == datetime.strptime("09:30", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=0)
    elif begin == datetime.strptime("12:50", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=50)
    elif begin == datetime.strptime("15:15", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=10)
    elif begin == datetime.strptime("17:55", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=5)
    elif begin == datetime.strptime("18:45", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=15)
    elif begin == datetime.strptime("18:55", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=5)
    else:
        begin = begin + timedelta(hours=0, minutes=10)
    return begin


def change_end_time(end):
    """subtract change"""
    if end == datetime.strptime("11:15", "%H:%M"):
        end = end - timedelta(hours=0, minutes=10)
    elif end == datetime.strptime("13:40", "%H:%M"):
        end = end - timedelta(hours=0, minutes=50)
    elif end == datetime.strptime("15:25", "%H:%M"):
        end = end - timedelta(hours=0, minutes=10)
    elif end == datetime.strptime("17:10", "%H:%M"):
        end = end - timedelta(hours=0, minutes=10)
    elif end == datetime.strptime("20:40", "%H:%M"):
        end = end - timedelta(hours=0, minutes=5)
    else:
        end = end - timedelta(hours=0, minutes=5)
    return end


def break_time(result_time):
    """divide time into 2 parts"""
    res = ["", ""]
    result_time = result_time.split("-")
    begin = datetime.strptime(result_time[0], "%H:%M")
    end = datetime.strptime(result_time[1], "%H:%M")
    res[0] = change_begin_time(begin).strftime('%H:%M')
    res[1] = change_end_time(end).strftime('%H:%M')
    return res


def add_in_answer(file, answer_mas, color_number):
    """add in answer array with color"""
    color_mas = ["#71AB7E", "#ffcc99", "#E3DD95", "#6D6D6e", "#F1B7B3",
                 "#B8A8CC", "#99ccff", "#73d978", "#ccff66"]
    with open(file, encoding="utf8") as open_file:
        read = json.load(open_file)
    for num in read:
        color_number += 1
        for i in read[num]:
            for j in read[num][i]:
                color = color_mas[color_number % 9]
                add_json_answer(i.split(', ')[1], j['time_begin'], j['time_end'],
                                answer_mas, color, num)


def check_answer_empty(answer_mas, file_teacher, file_student):
    """add in answer if failed to merge"""
    if not answer_mas:
        add_in_answer(file_student, answer_mas, 0)
        add_in_answer(file_teacher, answer_mas, 5)


def delete_repeat(answer_mas):
    """delete repeat in answer"""
    i = 1
    while i <= len(answer_mas) - 1:
        if answer_mas[i] == answer_mas[i - 1]:
            answer_mas.pop(i)
        else:
            i += 1


def main(flag):
    """define result"""
    file_teacher = 'static/json/teacher.json'
    file_student = 'static/json/student.json'
    free = 'static/json/free_time.json'
    answer = 'static/json/answer.json'

    free_time_mas = {"teacher": {}, "student": {}}
    free_time(file_teacher, "teacher", free_time_mas, flag)  # &&&&&&&&&&&&&&&&&&&
    free_time(file_student, "student", free_time_mas, flag)
    write_json_file(free, free_time_mas)
    answer_mas = []
    find_common_time(free, free_time_mas, answer_mas, flag)
    check_answer_empty(answer_mas, file_teacher, file_student)
    delete_repeat(answer_mas)
    write_json_file(answer, answer_mas)


if __name__ == '__main__':
    main("False")
