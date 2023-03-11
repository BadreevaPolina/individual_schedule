import re
import json

from bs4 import BeautifulSoup
import requests


def add_json(full_name, post, department, index, choice):
    one_str = {'full_name': full_name, 'post': post, 'department': department, 'index': index}
    choice['teacher'].append(one_str)


def write_json_file(file, data):
    with open(file, "w", encoding='utf-8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent=4)


def find_teachers(soup, user_input):
    teachers = []
    teacher_name = soup.find_all("div", class_="col-sm-3")
    for elem, name in enumerate(teacher_name):
        name = teacher_name[elem].text.strip()
        if user_input == name:
            teachers.append((name, elem))
    return teachers


def find_teacher_post(soup, elem):
    post = soup.find_all("div", class_="col-sm-2")
    return post[elem].get_text().strip()


def find_teacher_department(soup, elem):
    department = soup.find_all("div", class_="col-sm-7")
    return department[elem].get_text().strip()


def find_teacher_index(soup, elem):
    count = 0
    for tag_a in soup.find_all(onclick=True):
        line = str(tag_a['onclick'])
        result = re.findall(r"[0-9]+", line)
        if count == elem:
            return result[0]
        count += 1
    return ""


def find_info_teachers(teachers, soup, user_input, choice):
    for teacher in teachers:
        teacher_index_array = teacher[1]
        post = find_teacher_post(soup, teacher_index_array)
        department = find_teacher_department(soup, teacher_index_array)
        index = find_teacher_index(soup, teacher_index_array)
        add_json(user_input, post, department, index, choice)
        write_json_file('static/json/info_teacher.json', choice)


def main_teacher(teacher_target):
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }

    choice = {"teacher": []}

    user_input = teacher_target
    name_list = user_input.split(sep=' ')
    surname = name_list[0]
    url = 'https://timetable.spbu.ru/EducatorEvents/Index?q=' + surname
    wbdata = requests.get(url, cookies=cookie, timeout=10).text
    soup = BeautifulSoup(wbdata, 'lxml')

    teachers = find_teachers(soup, user_input)
    find_info_teachers(teachers, soup, user_input, choice)


if __name__ == '__main__':
    main_teacher("Смирнов Михаил Николаевич")
