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
        index = id_student(g, group)
        if index != "":
            return index
    return ""


def parse_group(index_year, group):
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    url_year_page = 'https://timetable.spbu.ru/MATH/StudyProgram/' + index_year
    url_year_page_ru = requests.get(url_year_page, cookies=cookie).text
    html_year_page = BeautifulSoup(url_year_page_ru, "lxml")
    return current_year(html_year_page, group)


def find_group(a, group):
    title = a['title'].split(", ")
    for group_in_title in title:
        if group == group_in_title:
            href_year = a['href'].split('/')
            return href_year[3]
    return ""


def find_year(html_main_page, group):
    year_group = "20" + group.split(".Б")[0]
    for a in html_main_page.find_all('a', href=True, title=True):
        title_year = a.text.strip()
        if title_year == year_group:
            href_index = find_group(a, group)
            if href_index != "":
                parse = parse_group(href_index, group)
                return parse
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
