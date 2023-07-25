import unittest

from free_time import *


class FreeTimeTest(unittest.TestCase):
    def test_compare_place(self):
        person1 = {'day': 'суббота',
                   'day_month': '24 июня',
                   'time_begin': '11:35',
                   'place_begin': 'Университетский проспект',
                   'time_end': '20:40',
                   'place_end': 'Университетский проспект'}
        person2 = {'day': 'суббота',
                   'day_month': '24 июня',
                   'time_begin': '09:30',
                   'place_begin': 'Университетский проспект',
                   'time_end': '15:00',
                   'place_end': 'Университетский проспект'}
        self.assertEqual(compare_place(person1, person2, "False"), "11:35-15:00")

        person1 = {'day': 'суббота',
                   'day_month': '24 июня',
                   'time_begin': '11:15',
                   'place_begin': 'Другой проспект',
                   'time_end': '20:40',
                   'place_end': 'Университетский проспект'}
        person2 = {'day': 'суббота',
                   'day_month': '24 июня',
                   'time_begin': '09:30',
                   'place_begin': 'Университетский проспект',
                   'time_end': '15:00',
                   'place_end': 'Университетский проспект'}
        self.assertEqual(compare_place(person1, person2, "False"), "13:15-15:00")

        person1 = {'day': 'суббота',
                   'day_month': '24 июня',
                   'time_begin': '11:15',
                   'place_begin': 'Другой проспект',
                   'time_end': '20:40',
                   'place_end': 'Университетский проспект'}
        person2 = {'day': 'суббота',
                   'day_month': '24 июня',
                   'time_begin': '09:30',
                   'place_begin': 'Университетский проспект',
                   'time_end': '15:00',
                   'place_end': 'Другой проспект'}
        self.assertEqual(compare_place(person1, person2, "False"), "")

    def test_common_time(self):
        self.assertEqual(common_time('11:15', '13:15', '11:15', '13:15'), "11:15-13:15")
        self.assertEqual(common_time('9:30', '10:00', '11:15', '13:15'), "")
        self.assertEqual(common_time('9:30', '17:15', '11:15', '13:40'), "11:15-13:40")

    def test_change_time(self):
        person1 = {'day': 'суббота',
                   'day_month': '24 июня',
                   'time_begin': '11:15',
                   'place_begin': 'Другой проспект',
                   'time_end': '20:40',
                   'place_end': 'Университетский проспект'}

        person2 = {'day': 'суббота',
                   'day_month': '24 июня',
                   'time_begin': '09:30',
                   'place_begin': 'Университетский проспект',
                   'time_end': '15:00',
                   'place_end': 'Университетский проспект'}

        self.assertEqual(change_time(person1), ('13:15', '20:40'))
        self.assertEqual(change_time(person2), ('09:30', '15:00'))

    def test_check_common_time_persons(self):
        free_time_mas = \
            {'teacher': {'Person1':
                [
                    {'day': 'четверг',
                     'day_month': '29 июня',
                     'time_begin': '09:30',
                     'place_begin': 'Университетский проспект',
                     'time_end': '15:00',
                     'place_end': 'Университетский проспект'},
                    {'day': 'четверг',
                     'day_month': '29 июня',
                     'time_begin': '16:35',
                     'place_begin': 'Университетский проспект',
                     'time_end': '20:40',
                     'place_end': 'Университетский проспект'}],
                'Person2':
                    [
                        {'day': 'четверг',
                         'day_month': '29 июня',
                         'time_begin': '09:30',
                         'place_begin': 'Университетский проспект',
                         'time_end': '13:00',
                         'place_end': 'Университетский проспект'}
                    ]},
                'student': {
                    '21.Б15-мм': [
                        {'day': 'четверг', 'day_month': '29 июня', 'time_begin': '11:35',
                         'place_begin': 'Университетский проспект',
                         'time_end': '20:40', 'place_end': 'Университетский проспект'}],
                    '21.Б08-мм': [
                        {'day': 'вторник', 'day_month': '13 июня', 'time_begin': '09:30',
                         'place_begin': 'Университетский проспект',
                         'time_end': '13:00', 'place_end': 'Университетский проспект'}]}}

        answer = {'teacher': {'Person2': [
            {'day_month': '29 июня',
             'place_begin': 'Университетский проспект',
             'place_end': 'Университетский проспект',
             'time_begin': '09:30',
             'time_end': '13:00'}]},
            'student': {'21.Б08-мм': []}}
        check_common_time_persons(free_time_mas, "False")
        self.assertEqual(free_time_mas, answer)

        free_time_mas = {'teacher': {'Person1': [
            {'day': 'четверг',
             'day_month': '29 июня',
             'time_begin': '16:35',
             'place_begin': 'Университетский проспект',
             'time_end': '20:40',
             'place_end': 'Университетский проспект'}],
            'Person2':
                [
                    {'day': 'суббота',
                     'day_month': '17 июня',
                     'time_begin': '16:35',
                     'place_begin': 'Университетский проспект',
                     'time_end': '20:40',
                     'place_end': 'Университетский проспект'}]}}
        check_common_time_persons(free_time_mas, "False")
        self.assertEqual(free_time_mas, {'teacher': {'Person2': []}})
