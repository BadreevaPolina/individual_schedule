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


def add_json_free_time(day, begin, end, places, free_time_dict):
    """string add in free time file"""
    one_str = {'day': day.split(', ')[0], 'day_month': day.split(', ')[1],
               'time_begin': end, 'place_begin': places[0],
               'time_end': begin, 'place_end': places[1]}
    free_time_dict.append(one_str)


def format_time(time, date_title):
    """make a standard response time"""
    time_format = datetime.strptime(time, "%H:%M")
    time_change = date_title + timedelta(hours=time_format.hour, minutes=time_format.minute)
    time_str = time_change.strftime("%Y-%m-%dT%H:%M:%S")
    return time_str


def add_json_answer(day_month, time_begin, time_end, answer_list, color, title):
    """string add in response array"""
    date = date_week(day_month)
    date_title = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    if title == "":
        title = date_title.strftime("%d.%m.%Y")
    time_begin_str = format_time(time_begin, date_title)
    time_end_str = format_time(time_end, date_title)
    one_str = {'title': title, 'start': time_begin_str,
               'end': time_end_str, 'color': color}
    answer_list.append(one_str)


def add_json_unchanged(day_month, type_subject, subject, place, time_begin, time_end, answer_list, color, title):
    """string add in response array"""
    date = date_week(day_month)
    date_title = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    if title == "":
        title = date_title.strftime("%d.%m.%Y")
    time_begin_str = format_time(time_begin, date_title)
    time_end_str = format_time(time_end, date_title)
    full_place = place.split(',')
    if len(full_place) > 1:
        cab = full_place[len(full_place) - 1].strip()
        title = title + ", " + type_subject + ", каб. " + cab
    else:
        title = title + ", " + type_subject
    one_str = {'title': title, 'start': time_begin_str, 'end': time_end_str,
               'color': color, 'subject': subject, 'place': place}
    answer_list.append(one_str)


def write_json_file(file, tables):
    """add response array in file"""
    with open(file, "w", encoding="utf8") as out_file:
        json.dump(tables, out_file, ensure_ascii=False, indent=4)


def free_time(file, person, free_time_dict, flag, place_university):
    """free time for person"""
    with open(file, encoding="utf8") as open_file:
        data = json.load(open_file)
        for num in data:
            free_time_dict[person][num] = []
            for day in data[num]:
                prev = None
                end = "09:30"
                for i in data[num][day]:
                    begin = i['time_begin']
                    # end first lesson, begin second lesson
                    if prev is not None and prev['time_begin'] == i['time_begin']:
                        if prev['time_end'] > i['time_end']:
                            i['time_end'] = prev['time_end']
                    elif prev is not None and prev['time_end'] == i['time_end']:
                        if prev['time_begin'] <= i['time_begin']:
                            i['time_begin'] = prev['time_begin']
                        else:
                            free_time_dict[person][num].pop()
                    estimate_time(end, begin, day, person, num, free_time_dict, flag, place_university)
                    end = i['time_end']
                    prev = i.copy()
                estimate_time(end, "20:40", day, person, num, free_time_dict, flag, place_university)


def estimate_time(end_time, begin_time, day, person, num, free_time_dict, flag, place_university):
    """check if the time is fits"""
    end = datetime.strptime(end_time, "%H:%M")
    begin = datetime.strptime(begin_time, "%H:%M")
    if begin - end >= timedelta(hours=1, minutes=45):
        if flag == "True":
            places = ["", ""]
            add_json_free_time(day, begin_time, end_time, places,
                               free_time_dict[person][num])
        else:
            places = check_place(end_time, begin_time, day, person, num, place_university)
            if places[0] == places[1]:
                add_json_free_time(day, begin_time, end_time,
                                   places, free_time_dict[person][num])
            else:
                if begin - end >= timedelta(hours=3, minutes=45):
                    add_json_free_time(day, begin_time, end_time,
                                       places, free_time_dict[person][num])


def check_place(end, begin, day, person, num, place_university):  # end first lesson, begin second lesson
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
            place[1] = place_university
        if end == "09:30":
            place[0] = place_university
    return place


def change_json_free_time(day, time_begin, time_end, place, free_time_dict):
    """change free time array """
    one_str = {'day_month': day,
               'time_begin': time_begin, 'place_begin': place,
               'time_end': time_end, 'place_end': place}
    free_time_dict.append(one_str)


def check_common_time_persons(free_time_dict, flag, place_university):
    """check common time teacher(student) and teacher(student)"""
    for _, person_i in enumerate(free_time_dict):
        keys = free_time_dict[person_i].keys()
        key_list = []
        for k in keys:
            key_list.append(k)
        for p in range(len(key_list) - 1):
            person1_dict = free_time_dict[person_i][key_list[p]]
            person2_dict = free_time_dict[person_i][key_list[p + 1]]

            free_time_dict[person_i].pop(key_list[p])
            free_time_dict[person_i].pop(key_list[p + 1])

            free_time_dict[person_i][key_list[p + 1]] = []
            for person1 in person1_dict:
                day_check = False
                for person2 in person2_dict:
                    if person1['day_month'] == person2['day_month']:
                        day_check = True
                        result_time = compare_place(person1, person2, flag, place_university)
                        if result_time != "":
                            time_b, time_e = break_time(result_time)
                            if time_b != time_e:
                                time_begin, time_end = result_time.split("-")
                                change_json_free_time(person1['day_month'], time_begin,
                                                      time_end, place_university,
                                                      free_time_dict[person_i][key_list[p + 1]])
                if person_i == "student":
                    if not day_check:
                        change_json_free_time(person1['day_month'], person1['time_begin'],
                                              person1['time_end'], place_university,
                                              free_time_dict[person_i][key_list[p + 1]])
                    person2_dict[:] = [person2 for person2 in person2_dict if person1['day_month'] != person2['day_month']]
            if person_i == "student":
                for person2 in person2_dict:
                    change_json_free_time(person2['day_month'], person2['time_begin'],
                                          person2['time_end'], place_university,
                                          free_time_dict[person_i][key_list[p + 1]])


def free_time_in_answer(free_time_dict, answer_list):
    """make response a free time file"""
    color_list = ["#71AB7E", "#ffcc99", "#E3DD95", "#6D6D6e", "#F1B7B3",
                  "#B8A8CC", "#99ccff", "#73d978", "#ccff66"]
    color_number = 0
    count = len(free_time_dict['student']) + len(free_time_dict['teacher'])
    for i in free_time_dict:
        color_number += 1
        for j in free_time_dict[i]:
            for k in free_time_dict[i][j]:
                if count == 1:
                    color = "#4e8bb1"
                else:
                    color = color_list[color_number % 9]
                add_json_answer(k['day_month'], k['time_begin'],
                                k['time_end'], answer_list, color, "")


def break_time_in_dict(free_time_dict):
    """change break time"""
    for i in free_time_dict:
        for k in free_time_dict[i]:
            for j in free_time_dict[i][k]:
                j["time_begin"], j["time_end"] = break_time(j["time_begin"] + "-" + j["time_end"])


def find_common_time(free, free_time_dict, answer_list, flag, place_university):
    """find common time depending on the situation"""
    with open(free, encoding="utf8") as file:
        read = json.load(file)
    if len(read["teacher"]) == len(read["student"]) == 1:
        check_common_time_s_t(free, answer_list, flag, True, place_university)
    elif (len(read["teacher"]) > 0 and len(read["student"]) == 0) or \
            (len(read["student"]) > 0 and len(read["teacher"]) == 0):
        check_common_time_persons(free_time_dict, flag, place_university)
        break_time_in_dict(free_time_dict)
        write_json_file(free, free_time_dict)
        free_time_in_answer(free_time_dict, answer_list)
    elif len(read["teacher"]) > 0 and len(read["student"]) > 0:
        check_common_time_persons(free_time_dict, flag, place_university)
        write_json_file(free, free_time_dict)
        check_common_time_s_t(free, answer_list, flag, True, place_university)


def check_common_time_s_t(free, answer_list, flag, with_day_check, place_university):
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
                        result_time = compare_place(i, j, flag, place_university)
                        if result_time != "":
                            time_begin, time_end = break_time(result_time)
                            if time_begin != time_end:
                                add_json_answer(i['day_month'], time_begin, time_end, answer_list, color, "")
            if not day_check and with_day_check:
                result_time = common_time(i['time_begin'], i['time_end'], "09:30", "20:40")
                if result_time != "":
                    time_begin, time_end = break_time(result_time)
                    if time_begin != time_end:
                        add_json_answer(i['day_month'], time_begin, time_end, answer_list, color, "")


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


def compare_place(person1, person2, flag, place_university):
    if flag == "False":
        b_1, e_1 = change_time(person1, place_university)
        b_2, e_2 = change_time(person2, place_university)
        return common_time(b_1, e_1, b_2, e_2)
    else:
        return common_time(person1['time_begin'], person1['time_end'],
                           person2['time_begin'], person2['time_end'])


def change_time(person, place_university):
    begin = datetime.strptime(person['time_begin'], "%H:%M")
    end = datetime.strptime(person['time_end'], "%H:%M")
    if person['place_begin'] != place_university:
        begin = begin + timedelta(hours=2, minutes=0)
    if person['place_end'] != place_university:
        end = end - timedelta(hours=2, minutes=0)
    return begin.strftime('%H:%M'), end.strftime('%H:%M')


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
    begin_new = change_begin_time(begin)
    end = datetime.strptime(result_time[1], "%H:%M")
    end_new = change_end_time(end)
    if end_new - begin_new >= timedelta(hours=1, minutes=35):
        res[0] = begin_new.strftime('%H:%M')
        res[1] = end_new.strftime('%H:%M')
    return res


def add_in_answer(file, answer_list, color_number):
    """add in answer array with color"""
    color_list = ["#71AB7E", "#ffcc99", "#E3DD95", "#6D6D6e", "#F1B7B3",
                  "#B8A8CC", "#99ccff", "#73d978", "#ccff66"]
    with open(file, encoding="utf8") as open_file:
        read = json.load(open_file)
    for num in read:
        color_number += 1
        for i in read[num]:
            for j in read[num][i]:
                color = color_list[color_number % 9]
                add_json_unchanged(i.split(', ')[1], j['type_subject'], j['subject'],
                                   j['full_place'], j['time_begin'], j['time_end'],
                                   answer_list, color, num)


def check_answer_empty(answer_list, file_teacher, file_student):
    """add in answer if failed to merge"""
    if not answer_list:
        add_in_answer(file_student, answer_list, 0)
        add_in_answer(file_teacher, answer_list, 5)


def delete_repeat(timetable_unchanged_list):  # что делать если разные здания
    """delete repeat in answer"""
    i = 1
    while i <= len(timetable_unchanged_list) - 1:
        answer1, answer2 = timetable_unchanged_list[i].copy(), timetable_unchanged_list[i - 1].copy()
        title1, title2 = answer1['title'].split(",", 2), answer2['title'].split(",", 2)
        place1, place2 = answer1['place'].split(",", 1), answer2['place'].split(",", 1)
        places = "," + place1[len(place1) - 1] + ",\n" + place2[len(place2) - 1]
        cabs = "," + title1[len(title1) - 1] + "," + title2[len(title2) - 1]

        answer1['title'], answer2['title'] = ",".join(title2[:2]), ",".join(title2[:2])
        answer1['place'], answer2['place'] = ",".join(place1[:1]), ",".join(place2[:1])

        if timetable_unchanged_list[i] == timetable_unchanged_list[i - 1]:
            timetable_unchanged_list.pop(i)
        elif answer1 == answer2:
            answer1['title'] = answer1['title'] + cabs
            answer1['place'] = answer1['place'] + places
            timetable_unchanged_list[i - 1] = answer1
            timetable_unchanged_list.pop(i)

        else:
            i += 1


def timetable_unchanged(timetable_unchanged_list, file_teacher, file_student):
    add_in_answer(file_student, timetable_unchanged_list, 0)
    add_in_answer(file_teacher, timetable_unchanged_list, 5)


def main(flag):
    """define result"""
    file_teacher = 'static/json/teacher.json'
    file_student = 'static/json/student.json'
    free = 'static/json/free_time.json'
    answer = 'static/json/answer.json'
    unchanged_time = 'static/json/timetable_unchanged.json'

    free_time_dict = {"teacher": {}, "student": {}}
    place_university = "Университетский проспект"
    free_time(file_teacher, "teacher", free_time_dict, flag, place_university)
    free_time(file_student, "student", free_time_dict, flag, place_university)
    write_json_file(free, free_time_dict)
    answer_list = []
    find_common_time(free, free_time_dict, answer_list, flag, place_university)
    write_json_file(answer, answer_list)

    timetable_unchanged_list = []
    timetable_unchanged(timetable_unchanged_list, file_teacher, file_student)
    delete_repeat(timetable_unchanged_list)
    write_json_file(unchanged_time, timetable_unchanged_list)


if __name__ == '__main__':
    main("False")
