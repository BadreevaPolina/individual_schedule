import unittest

from teacher_info_manager import *


class TeacherInfoManagerTest(unittest.TestCase):

    def test_find_teachers_1(self):
        info_teacher_instance = TeacherInfoManager()
        name = "Кир Я А"
        self.assertEqual(
            info_teacher_instance.main_teacher(name),
            (
                "Кир Я А, ",
                "",
                {
                    "teacher": [
                        {
                            "full_name": "Кириленко Яков Александрович",
                            "post": "старший преподаватель",
                            "department": "Кафедра системного программирования",
                            "index": "2690",
                        }
                    ]
                },
            ),
        )

    def test_find_teachers_2(self):
        info_teacher_instance = TeacherInfoManager()
        name = "Кириленко, Зеленчук"
        self.assertEqual(
            info_teacher_instance.main_teacher(name),
            ('Кириленко, Зеленчук, ', '', {'teacher': [
                {'full_name': 'Кириленко Демид Александрович', 'post': 'ведущий научный сотрудник',
                 'department': 'Кафедра физики твердого тела', 'index': '2167576'},
                {'full_name': 'Кириленко Яков Александрович', 'post': 'старший преподаватель',
                 'department': 'Кафедра системного программирования', 'index': '2690'},
                {'full_name': 'Зеленчук Илья Валерьевич', 'post': 'старший преподаватель',
                 'department': 'Кафедра системного программирования', 'index': '5587'}]}),
        )

    def test_find_teachers_3(self):
        info_teacher_instance = TeacherInfoManager()
        name = "Ошибка"
        self.assertEqual(
            info_teacher_instance.main_teacher(name),
            ('', 'Ошибка, ', {'teacher': []}),
        )
