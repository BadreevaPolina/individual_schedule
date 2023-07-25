import unittest

from find_teacher_json import *


def help_find(teacher):
    cookie = {
        "_culture": "ru",
        "value": "ru"
    }
    user_input = teacher.lower().strip()
    name_list = user_input.split(sep=' ')
    surname = name_list[0]
    url = 'https://timetable.spbu.ru/EducatorEvents/Index?q=' + surname
    wbdata = requests.get(url, cookies=cookie, timeout=10).text
    soup = BeautifulSoup(wbdata, 'lxml')
    return soup, user_input


def get_soups_and_users_input(names):
    soups, users_input = [], []
    for name in names:
        soup, user_input = help_find(name)
        soups.append(soup)
        users_input.append(user_input)
    return soups, users_input


class FindTeacherJsonTest(unittest.TestCase):

    def test_find_teachers(self):
        names = ["Кириленко", "Луцив", "Vorobyov"]
        soups, users_input = get_soups_and_users_input(names)

        self.assertEqual(find_teachers(soups[0], users_input[0]),
                         [('Кириленко Демид Александрович', 0),
                          ('Кириленко Яков Александрович', 1)])
        self.assertEqual(find_teachers(soups[1], users_input[1]),
                         [('Луцив Дмитрий Вадимович', 0)])
        self.assertEqual(find_teachers(soups[2], users_input[2]),
                         [])

    def test_find_teacher_info(self):
        names = ["Кириленко", "Луцив"]
        soups, users_input = get_soups_and_users_input(names)

        teacher = find_teachers(soups[0], users_input[0])
        if len(teacher) >= 2:
            teacher_index_array = teacher[1][1]
            self.assertEqual(find_teacher_post(soups[0], teacher_index_array), "старший преподаватель")
            self.assertEqual(find_teacher_department(soups[0], teacher_index_array), "Кафедра системного программирования")
            self.assertEqual(find_teacher_index(soups[0], teacher_index_array), "2690")

        teacher = find_teachers(soups[1], users_input[1])
        teacher_index_array = teacher[0][1]
        self.assertEqual(find_teacher_post(soups[1], teacher_index_array), "доцент")
        self.assertEqual(find_teacher_department(soups[1], teacher_index_array), "Кафедра системного программирования")
        self.assertEqual(find_teacher_index(soups[1], teacher_index_array), "2760")