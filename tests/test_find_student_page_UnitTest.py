import unittest

from find_student_page import *


class FindStudentPageTest(unittest.TestCase):
    def test_main_student(self):
        self.assertEqual(main_student("21.Б15-мм"), "334764")
        self.assertEqual(main_student("22.М09-мм"), "334896")
        self.assertEqual(main_student("20.А04-мм"), "335360")
        self.assertEqual(main_student("22.С03-мм"), "334447")

        self.assertEqual(main_student("14.Е15-мм"), "")
        self.assertEqual(main_student("14.Е"), "")
        self.assertEqual(main_student(""), "")
