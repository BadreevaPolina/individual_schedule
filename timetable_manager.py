"""jsons with timetable information"""
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests


class TimetableManager:
    def __init__(self):
        self.incorrect_time = {"student": [], "teacher": []}
        self.timetable = {"student": {}, "teacher": {}}

    def add_json(
        self, day, date, times, place, subject, person, name, type_subject, full_place
    ):
        """string add in response array"""
        if day:
            self.timetable[person][name][day + ", " + date] = []
            for i, time in enumerate(times):
                time, incorrect_time_event = self.correct_time(time, date, name)
                if incorrect_time_event != "":
                    self.incorrect_time[person].append(incorrect_time_event)
                one_str = {
                    "time_begin": time[0],
                    "time_end": time[1],
                    "place": place[i],
                    "full_place": full_place[i],
                    "subject": subject[i],
                    "type_subject": type_subject[i],
                }
                self.timetable[person][name][day + ", " + date].append(one_str)

    @staticmethod
    def correct_time(times, date, name):
        """write correct time"""
        time = times.split("\u2013")
        if len(time) == 2:
            return time, ""
        begin = datetime.strptime(time[0], "%H:%M")
        end = begin + timedelta(hours=1, minutes=35)
        return [
            begin.strftime("%H:%M"),
            end.strftime("%H:%M"),
        ], "Не указано время конца пары " + date + " в " + begin.strftime(
            "%H:%M"
        ) + " - " + name + ". Предполагается, что занятие будет длиться 1:35."

    @staticmethod
    def find_subject(panel):
        name_subjects = []
        type_subjects = []
        subjects = panel.find_all("span", title="Предмет")
        if subjects is not None:
            for subject in subjects:
                type_sub = subject.get_text().split(",")
                if len(type_sub) != 1:
                    type_subject = type_sub[1]
                    name_subject = type_sub[0]
                else:
                    type_subject = type_sub[0]
                    name_subject = ""
                name_subjects.append(name_subject.strip().replace("\r\n", ", "))
                type_subjects.append(type_subject.strip().replace("\r\n", ""))
        return name_subjects, type_subjects

    def find_info(self, soup, person, name):
        """collect all information"""
        panels = soup.findAll(class_="panel panel-default")
        for panel in panels:
            title = self.find_day(panel)
            times = self.find_time(panel)
            places, full_places = self.find_place(panel)
            subjects, type_subjects = self.find_subject(panel)
            if title is not None and times:
                day = title[0]
                date = title[1]
                self.add_json(
                    day,
                    date,
                    times,
                    places,
                    subjects,
                    person,
                    name,
                    type_subjects,
                    full_places,
                )

    @staticmethod
    def find_day(panel):
        """information about day"""
        days = panel.find_all("h4", class_="panel-title")
        for day_str in days:
            only_day = day_str.get_text().split(",")
            day_param, date_param = only_day[0].strip(), only_day[1].strip()
            title = [day_param.lower(), date_param.lower()]
            return title

    @staticmethod
    def find_time(panel):
        """information about time"""
        times = panel.find_all("span", title="Время")
        time_array = []
        for time in times:
            time_param = time.get_text().strip()
            time_array.append(time_param)
        return time_array

    @staticmethod
    def find_place(panel):
        """information about place"""
        places = panel.findAll(
            True,
            {
                "class": [
                    "col-sm-3 studyevent-locations",
                    "col-sm-3 studyevent-multiple-locations",
                ]
            },
        )
        place_array = []
        full_place_array = []
        for place in places:
            street = place.get_text().split(",")
            full_place = place.get_text().strip().split("\r\n")
            place_param = street[0].strip()
            place_array.append(place_param)
            full_place_array.append(full_place[0])
        return place_array, full_place_array

    @staticmethod
    def today_week():
        """define the start date of this week"""
        today = datetime.now().date()
        date = today - timedelta(datetime.now().weekday())
        return date

    @staticmethod
    def few_weeks(self, count_weeks):
        """write the beginning of several weeks"""
        weeks = []
        this_week = self.today_week()
        for i in range(0, count_weeks):
            date = this_week + timedelta(weeks=i)
            weeks.append(date)
        return weeks

    def info_schedule(self, person, name, url, count_weeks):
        """info about schedule for several weeks"""
        cookie = {"_culture": "ru", "value": "ru"}
        weeks = self.few_weeks(self, count_weeks)
        for week in weeks:
            url_person = url + str(week)
            url_person_ru = requests.get(url_person, cookies=cookie, timeout=15).text
            html_person = BeautifulSoup(url_person_ru, "lxml")
            self.find_info(html_person, person, name)

    def get_info_about_person(self, person, href, input_index, name, count_weeks):
        persons_index = input_index.split(",")
        for i, index in enumerate(persons_index):
            if index not in ("", " "):
                url_person = href + index.strip() + "/"
                self.timetable[person][name[i]] = {}
                self.info_schedule(person, name[i], url_person, count_weeks)

    def main_teacher(self, input_index, name, count_weeks=4):
        """json with teachers timetable information"""
        href = "https://timetable.spbu.ru/WeekEducatorEvents/"
        person = "teacher"
        try:
            self.get_info_about_person(person, href, input_index, name, count_weeks)
        except Exception as e:
            logging.exception(e)

    def main_student(self, input_index, name, count_weeks=4):
        """json with students timetable information"""
        self.timetable = {"student": {}, "teacher": {}}
        self.incorrect_time = {"student": [], "teacher": []}
        href = "https://timetable.spbu.ru/MATH/StudentGroupEvents/Primary/"
        person = "student"
        try:
            self.get_info_about_person(person, href, input_index, name, count_weeks)
        except Exception as e:
            logging.exception(e)
