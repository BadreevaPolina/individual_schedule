import re
import json

from bs4 import BeautifulSoup
import requests


def add_json(full_name, post, department, index, choice):
    one_str = {'full_name': full_name, 'post': post, 'department': department, 'index': index}
    choice["teacher"].append(one_str)


def write_json_file(file, data):
    with open(file, "w", encoding='utf-8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent=4)


def find_teachers(soup, user_input):
    teachers = []
    teacher_name = soup.find_all("div", class_="col-sm-3")
    for elem, name in enumerate(teacher_name):
        name = teacher_name[elem].text.strip()
        if user_input == name[: len(user_input)].lower():
            teachers.append((name, elem))
        else:
            user_target = user_input.split(" ")
            users = name.lower().split(" ")
            if len(user_target) == len(users):
                if user_target[0] == users[0] and user_target[1] == users[1][: len(user_target[1])] \
                        and user_target[2] == users[2][: len(user_target[2])]:
                    teachers.append((name, elem))
    return teachers


def find_teacher_post(soup, elem):
    post = soup.find_all("div", class_="col-sm-2")
    return post[elem].get_text().strip().replace("\r\n", ", ")


def find_teacher_department(soup, elem):
    department = soup.find_all("div", class_="col-sm-7")
    return department[elem].get_text().strip().replace("\r\n", ", ")


def find_teacher_index(soup, elem):
    count = 0
    for tag_a in soup.find_all(onclick=True):
        line = str(tag_a['onclick'])
        result = re.findall(r"[0-9]+", line)
        if count == elem:
            return result[0]
        count += 1
    return ""


def find_info_teachers(teachers, soup, choice):
    for teacher in teachers:
        teacher_index_array = teacher[1]
        post = find_teacher_post(soup, teacher_index_array)
        department = find_teacher_department(soup, teacher_index_array)
        index = find_teacher_index(soup, teacher_index_array)
        add_json(teacher[0], post, department, index, choice)


def main_teacher(teacher_target):
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }

    choice = {"teacher": []}
    teachers_target = teacher_target.split(",")
    for teacher in teachers_target:
        user_input = teacher.lower().strip()
        name_list = user_input.split(sep=' ')
        surname = name_list[0]
        url = 'https://timetable.spbu.ru/EducatorEvents/Index?q=' + surname
        wbdata = requests.get(url, cookies=cookie, timeout=10).text
        soup = BeautifulSoup(wbdata, 'lxml')

        teachers = find_teachers(soup, user_input)
        find_info_teachers(teachers, soup, choice)
    write_json_file('static/json/info_teacher.json', choice)


if __name__ == '__main__':
    main_teacher("Смирнов Михаил Николаевич, Кириленко Я А")
