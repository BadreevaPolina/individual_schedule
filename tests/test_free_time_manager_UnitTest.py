import unittest

from free_time_manager import *


class FreeTimeManagerTest(unittest.TestCase):

    def test_change_time(self):
        free_time = FreeTimeManager()
        timetable = {
            "student": {
                "1": {
                    "суббота, 11 октября": [
                        {
                            "time_begin": "11:15",
                            "time_end": "13:40",
                            "place": "Университетский проспект",
                            "full_place": "Университетский проспект, д. 28, лит. В,3389",
                            "subject": "Дискретная математика",
                            "type_subject": "практическое занятие",
                        }
                    ]
                }
            },
            "teacher": {
                "2": {
                    "суббота, 11 октября": [
                        {
                            "time_begin": "12:10",
                            "time_end": "15:15",
                            "place": "Университетский проспект",
                            "full_place": "Университетский проспект, д. 28, лит. В,3389",
                            "subject": "Дискретная математика",
                            "type_subject": "практическое занятие",
                        }
                    ]
                }
            },
        }
        result_answer_list = [
            {
                "color": "#4e8bb1",
                "end": "2023-10-11T11:05:00",
                "start": "2023-10-11T09:30:00",
                "title": "11.10.2023",
            },
            {
                "color": "#4e8bb1",
                "end": "2023-10-11T20:35:00",
                "start": "2023-10-11T15:25:00",
                "title": "11.10.2023",
            },
        ]
        result_timetable_unchanged_list = [
            {
                "color": "#ffcc99",
                "end": "2023-10-11T13:40:00",
                "place": "Университетский проспект, д. 28, лит. В,3389",
                "start": "2023-10-11T11:15:00",
                "subject": "Дискретная математика",
                "title": "1, практическое занятие, каб. 3389",
            },
            {
                "color": "#E3DD95",
                "end": "2023-10-11T15:15:00",
                "place": "Университетский проспект, д. 28, лит. В,3389",
                "start": "2023-10-11T12:10:00",
                "subject": "Дискретная математика",
                "title": "2, практическое занятие, каб. 3389",
            },
        ]

        free_time.main("False", timetable)
        self.assertEqual(free_time.answer_list, result_answer_list)
        self.assertEqual(
            free_time.timetable_unchanged_list, result_timetable_unchanged_list
        )
