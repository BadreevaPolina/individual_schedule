import re

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json
#from flask import jsonify, request
import main

cookie = {
    "_culture": "ru",
    "value": "ru"
}


choice = {"teacher": []}
one_str = {}


def add_json(full_name, post, department, index):
        one_str = {'full_name': full_name, 'post': post, 'department': department, 'index': index}
        choice['teacher'].append(one_str)



def write_json_file(file, data):
    out_file = open(file, "w")
    json.dump(data, out_file, ensure_ascii=False, indent=4)
    out_file.close()

def find_teacher(soup):
    teachers = []
    teacher_name = soup.find_all("div", class_="col-sm-3")
    for elem in range(len(teacher_name)):
        l = teacher_name[elem].text.strip()
        if user_input == l:
            teachers.append(elem)
    return teachers


def find_teacher_post(soup, elem):
    post = soup.find_all("div", class_="col-sm-2")
    return post[elem].get_text().strip()


def find_teacher_department(soup, elem):
    department = soup.find_all("div", class_="col-sm-7")
    return department[elem].get_text().strip()


def find_teacher_index(soup, elem):
    count = 0
    for a in soup.find_all(onclick=True):
        line = (str)(a['onclick'])
        result = re.findall(r"[0-9]+", line)
        if count == elem:
            return result[0]
        count += 1


if __name__ == '__main__':
    print("Введите ФИО нужного преподавателя")
    user_input = main.input_form
    name_list = user_input.split(sep=' ')
    surname = name_list[0]

    url = 'https://timetable.spbu.ru/EducatorEvents/Index?q=' + surname
    wbdata = requests.get(url, cookies=cookie).text
    soup = BeautifulSoup(wbdata, 'lxml')

    teachers = find_teacher(soup)

    if teachers:
        for elem in find_teacher(soup):
            post = find_teacher_post(soup, elem)
            department = find_teacher_department(soup, elem)
            index = find_teacher_index(soup, elem)
            add_json(user_input, post, department, index)
        write_json_file('info_teacher.json', choice)
    else:
        print("Ошибка. Такой преподаватель не найден. Попробуйте ещё раз.")