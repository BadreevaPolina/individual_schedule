"""information about suitable teachers"""
import logging
import re

from bs4 import BeautifulSoup
import requests


class TeacherInfoManager:
    def __init__(self):
        self.info_teacher = {"teacher": []}

    def add_json(self, full_name, post, department, index):
        """string add in response array"""
        one_str = {
            "full_name": full_name,
            "post": post,
            "department": department,
            "index": index,
        }
        self.info_teacher["teacher"].append(one_str)

    @staticmethod
    def find_teachers(soup, user_input):
        """collect all suitable teachers"""
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
                    if (
                        user_target[0] == users[0][: len(user_target[0])]
                        and user_target[1] == users[1][: len(user_target[1])]
                        and user_target[2] == users[2][: len(user_target[2])]
                    ):
                        teachers.append((name, elem))
                elif len(user_target) == len(users) - 1:
                    if (
                        user_target[0] == users[0][: len(user_target[0])]
                        and user_target[1] == users[1][: len(user_target[1])]
                    ):
                        teachers.append((name, elem))
        return teachers

    @staticmethod
    def find_teacher_post(soup, elem):
        """information about post"""
        post = soup.find_all("div", class_="col-sm-2")
        return post[elem].get_text().strip().replace("\r\n", ", ")

    @staticmethod
    def find_teacher_department(soup, elem):
        """information about department"""
        department = soup.find_all("div", class_="col-sm-7")
        return (
            department[elem].get_text().strip().replace("\r\n", ", ").replace('"', "")
        )

    @staticmethod
    def find_teacher_index(soup, elem):
        """information about index"""
        count = 0
        for tag_a in soup.find_all(onclick=True):
            line = str(tag_a["onclick"])
            result = re.findall(r"[0-9]+", line)
            if count == elem:
                return result[0]
            count += 1
        return ""

    def find_info_teachers(self, teachers, soup):
        """collect all information"""
        for teacher in teachers:
            teacher_index_array = teacher[1]
            post = self.find_teacher_post(soup, teacher_index_array)
            department = self.find_teacher_department(soup, teacher_index_array)
            index = self.find_teacher_index(soup, teacher_index_array)
            self.add_json(teacher[0], post, department, index)

    def main_teacher(self, teacher_target):
        """get information about suitable teachers"""
        cookie = {"_culture": "ru", "value": "ru"}

        self.info_teacher = {"teacher": []}
        teacher_input, teachers_error = "", ""
        teachers_target = teacher_target.strip().split(",")
        while "" in teachers_target:
            teachers_target.remove("")
        try:
            for teacher in teachers_target:
                user_input = teacher.lower().strip()
                name_list = user_input.split(sep=" ")
                surname = name_list[0]
                url = "https://timetable.spbu.ru/EducatorEvents/Index?q=" + surname
                wbdata = requests.get(url, cookies=cookie, timeout=15).text
                soup = BeautifulSoup(wbdata, "lxml")
                teachers = self.find_teachers(soup, user_input)
                if teachers:
                    teacher_input = teacher_input + teacher.strip() + ", "
                else:
                    teachers_error = teachers_error + teacher.strip() + ", "
                self.find_info_teachers(teachers, soup)
            return teacher_input, teachers_error, self.info_teacher
        except Exception as e:
            logging.exception(e)
            return None, None


if __name__ == "__main__":
    manager = TeacherInfoManager()
    print(manager.main_teacher("Кир Я А"))  # example
