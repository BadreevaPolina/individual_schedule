import unittest

from find_student_page import *


class FindStudentPageTest(unittest.TestCase):
    def test_main_student(self):
        self.assertEqual(main_student("21.Б15-мм"), "365898")
        self.assertEqual(main_student("22.М06-мм"), "366331")
        self.assertEqual(main_student("20.А04-мм"), "366379")
        self.assertEqual(main_student("22.С03-мм"), "365754")

        self.assertEqual(main_student("14.Е15-мм"), "")
        self.assertEqual(main_student("14.Е"), "")
        self.assertEqual(main_student(""), "")
