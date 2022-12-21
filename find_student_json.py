import json
from bs4 import BeautifulSoup
import requests


def id_student(html_year_page, group):
    groups = html_year_page.find_all(class_='tile', onclick=True)
    for g in groups:
        group_name = g.text.strip().split('\r\n')
        if str(group_name[0]) == str(group):
            line = str(g['onclick']).split('/')
            line = line[4].split("'")
            return line[0]
    return ""


def current_year(html_year_page, group):
    groups = html_year_page.find_all(id='studentGroupsForCurrentYear')
    for g in groups:
        number = id_student(g, group)
        if number != "":
            return number
    return ""


def find_group(index_year, group):
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    url_year_page = 'https://timetable.spbu.ru/MATH/StudyProgram/' + index_year
    url_year_page_ru = requests.get(url_year_page, cookies=cookie).text
    html_year_page = BeautifulSoup(url_year_page_ru, "lxml")
    return current_year(html_year_page, group)


def find_year(html_main_page, group):
    for a in html_main_page.find_all('a', href=True):
        href_year = a['href'].split('/')
        if len(href_year) == 4:
            number = find_group(href_year[3], group)
            if number != "":
                return number
    return ""


def main_student(group):
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    url_main_page = 'https://timetable.spbu.ru/MATH'
    url_main_page_ru = requests.get(url_main_page, cookies=cookie).text
    html_main_page = BeautifulSoup(url_main_page_ru, "lxml")
    number = find_year(html_main_page, group)
    return number
