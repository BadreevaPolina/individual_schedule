import unittest

from main import *


class MainTest(unittest.TestCase):
    def test_edit_input_students(self):
        self.assertEqual(edit_input_students("21.Б15-мм"), ('365898,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15"), ('365898,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("21Б15"), ('365898,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("21б15"), ('365898,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("21б15,,,,,,,,,"), ('365898,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("2115"), ('', '', '2115, '))

        self.assertEqual(edit_input_students("21.Б15, 21.Б11"), ('365898,365899,', '21.Б15-мм, 21.Б11-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15,      21.Б11"), ('365898,365899,', '21.Б15-мм, 21.Б11-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15,21.Б11"), ('365898,365899,', '21.Б15-мм, 21.Б11-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15 21.Б11"), ('365898,365899,', '21.Б15-мм, 21.Б11-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15   21.Б11"), ('365898,365899,', '21.Б15-мм, 21.Б11-мм, ', ''))

        self.assertEqual(edit_input_students("23.М06-мм"), ('365846,', '23.М06-мм, ', ''))
        self.assertEqual(edit_input_students("20.А04-мм"), ('366379,', '20.А04-мм, ', ''))
        self.assertEqual(edit_input_students("22.С03-мм"), ('365754,', '22.С03-мм, ', ''))

        self.assertEqual(edit_input_students("23.М06-мм, 20.А04-мм, 22.С03-мм"),
                         ('365846,366379,365754,', '23.М06-мм, 20.А04-мм, 22.С03-мм, ', ''))


