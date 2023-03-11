import json

from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

import find_student_page
import find_teacher_json
import free_time
import timetable_json

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def index():
    """main page"""
    return render_template('index.html')


def find_teacher(input_form):
    """information about teachers"""
    find_teacher_json.main_teacher(input_form)


def find_student(input_form):
    """information about id student"""
    id_student = find_student_page.main_student(input_form)
    timetable_json.main_student(id_student)


# def count_person(person):
#     persons = person.split(",")
#     return len(persons)
#

# def decide_compare(teachers, students):
#     teachers = teachers.split(",")
#     students = students.split(",")
#     if teachers != "" and students != "":
#         if len(teachers) == len(students) == 1:
#             find_student(students)
#             find_teacher(teachers)
#         else:
#             for teacher in teachers:
#                 find_teacher(teacher)  # add in file all teachers
#                 # new fun compare_teachers
#             for s in range(0, len(students)):
#                 students[s] = find_student_page.main_student(s)
#                 # new fun compare_students
#             # compare together
#     else:
#         if teachers != "" and students == "":
#             for teacher in teachers:
#                 find_teacher(teacher)
#                 # only teachers
#         if teachers == "" and students != "":
#             for student in students:
#                 find_student(student)
#                 # only students


@app.route('/find', methods=["GET", "POST"])
def find():
    """main page with information about teachers or return result timetable"""
    if request.method == 'POST':
        student = request.form.get('student')
        teacher = request.form.get('teacher')
        flag_place = 'flag_place' in request.form
        student_result = jsonify(student)
        find_student(student_result.json)
        teacher_result = jsonify(teacher)
        find_teacher(teacher_result.json)
        if one_teacher_table(str(flag_place)) is not None:
            return render_template('table.html')
        return render_template('index.html', student=student,
                               teacher=teacher, flag_place=flag_place,
                               checkbox_checked="checked" if flag_place else "")
    return render_template('index.html')


def one_teacher_table(flag):
    """if found one teacher, show result page"""
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data = json.load(file)
    res = data['teacher']
    if len(res) == 1:
        for i in res:
            if i['index']:
                result = i['index']
                timetable_json.main_teacher(result)
                free_time.main(flag)
                return result
    return None


def one_teacher():
    """if on the main mage is only one card - pull out the id"""
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data = json.load(file)
    res = data['teacher']
    for i in res:
        if i['index']:
            return i['index']
    return ""


@app.route("/time", methods=["GET", "POST"])
def timetable():
    """show result page"""
    result = request.form.get('id')
    flag = request.form.get('flag_place')
    if result == "":
        result = one_teacher()
    timetable_json.main_teacher(result)
    free_time.main(str(flag))
    return render_template('table.html')


if __name__ == '__main__':
    app.run(port=5000)
