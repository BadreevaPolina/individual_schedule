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
    return len(input_form.split(","))


def find_student(input_form):
    """information about id student"""
    students = input_form.split(",")
    id_students = ""
    for student in students:
        student = student.strip().upper()
        student = student.replace("-ММ", "-мм")
        if not "-мм" in student:
            student += "-мм"
        if not "." in student:
            student = student[:2] + "." + student[2:]
        id_student = find_student_page.main_student(student)
        id_students = id_students + id_student + ","
    timetable_json.main_student(id_students, students)


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
        count_teacher = find_teacher(teacher_result.json)
        if one_zero_teacher_table(str(flag_place)) is not None:
            return render_template('table.html')
        return render_template('index.html', student=student,
                               teacher=teacher, flag_place=flag_place,
                               checkbox_checked="checked" if flag_place else "",
                               count_teacher=count_teacher)
    return render_template('index.html')


def one_zero_teacher_table(flag):
    """if found one teacher, show result page"""
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data_t = json.load(file)
    with open("static/json/student.json", encoding="utf8") as file:
        data_s = json.load(file)
    if len(data_t['teacher']) == 0 and len(data_s) > 1:
        timetable_json.main_teacher("", [""])
        free_time.main(flag)
        return "ok"
    if len(data_t['teacher']) == 1:
        for i in data_t['teacher']:
            if i['index']:
                result = i['index']
                timetable_json.main_teacher(result, [i['full_name']])
                free_time.main(flag)
                return result
    return None


def name_teachers(index_teachers):
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data_t = json.load(file)
    index_teachers = index_teachers.split(", ")
    teachers = []
    for j, index_teacher in enumerate(index_teachers):
        for i in data_t['teacher']:
            if i['index'] == index_teacher:
                teachers = teachers + [i['full_name']]
    return teachers


@app.route("/time", methods=["GET", "POST"])
def timetable():
    """show result page"""
    flag_place = request.form.get('flag_place')
    index_teachers = request.form.get('index_teachers')
    teachers = name_teachers(index_teachers)
    timetable_json.main_teacher(index_teachers, teachers)
    free_time.main(str(flag_place))
    return render_template('table.html')


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
