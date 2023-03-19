import sqlite3
import time
from bs4 import BeautifulSoup
import requests
import json
from googletrans import Translator

def get_timetable():
    translator = Translator()

    # отправляем GET-запрос на страницу
    url = 'https://timetable.spbu.ru/MATH'
    params = {'class': 'locale-option', 'id': 'my-id', 'checked' : 'checked'}
    r = requests.get(url, params=params)

    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    table = []

    cursor.execute("CREATE TABLE IF NOT EXISTS timetable (time TEXT, subject TEXT,  room TEXT, teacher TEXT)")

    # используем BeautifulSoup для парсинга HTML-кода
    soup = BeautifulSoup(r.content, 'html.parser')

    # получаем все ссылки на странице
    links = soup.find_all('a')
    count = 0
    links_programs = []

    #переходим по каждой ссылке и парсим содержимое страницы
    for link in links:
        # получаем адрес ссылки
        if (link.get('href')[1:5] == 'MATH'):
            href = link.get('href')
            href = 'https://timetable.spbu.ru' + href
        else:
            continue
        count += 1
        links_programs.append(href)
    links_groups = []
    print(links_programs, len(links_programs))

    word = 'Attestation'
    for link in links_programs:

        # отправляем GET-запрос на страницу
        url = link
        r = requests.get(link)

        # используем BeautifulSoup для парсинга HTML-кода
        soup = BeautifulSoup(r.content, 'html.parser')

        # получаем все ссылки на странице
        tiles = soup.find_all(class_='tile', attrs={'onclick': True})
        # выводим найденные элементы

        for tile in tiles:
            onclick_value = tile.get('onclick')

        onclick_value = 'https://timetable.spbu.ru' + onclick_value[22:-1]
        if (word not in onclick_value) and ('358846' not in onclick_value) and ('335340' not in onclick_value) and ('334765' not in onclick_value) and ('334747' not in onclick_value):
            links_groups.append(onclick_value)
    print(links_groups, len(links_groups))

    for link in links_groups:
        url = link
        print(url)
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title
        panels = soup.findAll(class_='panel panel-default')
        panel_list = []
        for panel in panels:
            row = {}
            day_h4 = panel.find('h4')
            if day_h4:
                day = day_h4.text.split()
                row['Date'] = ' '.join(day)
                #print(' '.join(day), end=' ')

            times = panel.findAll(class_='col-sm-2 studyevent-datetime')
            subjects = panel.findAll(class_='col-sm-4 studyevent-subject')
            locations = panel.findAll(class_='col-sm-3 studyevent-locations')
            teachers = panel.findAll(class_='col-sm-3 studyevent-educators')


            #print(len(times), len(subjects), len(locations), len(teachers))
            for i in range(len(locations)):
                if day_h4:
                    string =' '.join(day) + ' ' + ' '.join(times[i].text.split()) + ' ' + ' '.join(subjects[i].text.split()) + ' ' + ' '.join(locations[i].text.split()) + ' ' + ' '.join(teachers[i].text.split())
                else:
                    string = ' '.join(times[i].text.split()) + ' '.join(subjects[i].text.split()) + ' '.join(locations[i].text.split()) + ' '.join(teachers[i].text.split())
                panel_list.append(string)
                day_e = ' '.join(day)
                time = ' '.join(times[i].text.split())
                subject = ' '.join(subjects[i].text.split())
                location = ' '.join(locations[i].text.split())
                teacher = ' '.join(teachers[i].text.split())

                if day_h4:
                    day_schedule = {
                        # 'time' : time,
                        # 'subject' : subject,
                        # 'location' : location,
                        # 'teacher' : teacher,
                        'date' : translator.translate(day_e, dest='ru').text,
                        'time' : translator.translate(time, dest='ru').text,
                        'subject' : translator.translate(subject, dest='ru').text,
                        'location' : translator.translate(location, dest='ru').text,
                        'teacher' : translator.translate(teacher, dest='ru').text,
                        'link' : url
                    }
                else:
                    day_schedule_1 = {
                        # 'time': time,
                        # 'subject': subject,
                        # 'location': location,
                        # 'teacher': teacher,
                        'time' : translator.translate(time, dest='ru').text,
                        'subject' : translator.translate(subject, dest='ru').text,
                        'location' : translator.translate(location, dest='ru').text,
                        'teacher' : translator.translate(teacher, dest='ru').text,
                        'link': url
                    }
                if day_h4:
                    table.append(day_schedule)
                else:
                    table.append(day_schedule_1)
                print(table)
        print(panel_list)

        with open("timetable_table.json", "w", encoding="utf-8") as file:
            json.dump(table, file, ensure_ascii=False, indent=4)

while True:
    get_timetable()
    time.sleep(24 * 60 * 60)
