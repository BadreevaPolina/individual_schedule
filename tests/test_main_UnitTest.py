import unittest

from main import *


class MainTest(unittest.TestCase):
    def test_edit_input_students(self):
        self.assertEqual(edit_input_students("21.Б15-мм"), ('334764,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15"), ('334764,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("21Б15"), ('334764,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("21б15"), ('334764,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("21б15,,,,,,,,,"), ('334764,', '21.Б15-мм, ', ''))
        self.assertEqual(edit_input_students("2115"), ('', '', '2115, '))

        self.assertEqual(edit_input_students("21.Б15, 21.Б11"), ('334764,334755,', '21.Б15-мм, 21.Б11-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15,      21.Б11"), ('334764,334755,', '21.Б15-мм, 21.Б11-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15,21.Б11"), ('334764,334755,', '21.Б15-мм, 21.Б11-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15 21.Б11"), ('334764,334755,', '21.Б15-мм, 21.Б11-мм, ', ''))
        self.assertEqual(edit_input_students("21.Б15   21.Б11"), ('334764,334755,', '21.Б15-мм, 21.Б11-мм, ', ''))

        self.assertEqual(edit_input_students("22.М09-мм"), ('334896,', '22.М09-мм, ', ''))
        self.assertEqual(edit_input_students("20.А04-мм"), ('335360,', '20.А04-мм, ', ''))
        self.assertEqual(edit_input_students("22.С03-мм"), ('334447,', '22.С03-мм, ', ''))

        self.assertEqual(edit_input_students("22.М09-мм, 20.А04-мм, 22.С03-мм"),
                         ('334896,335360,334447,', '22.М09-мм, 20.А04-мм, 22.С03-мм, ', ''))


