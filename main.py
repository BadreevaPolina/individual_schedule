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
    return render_template('index.html')


def find_teacher(input_form):
    find_teacher_json.main_teacher(input_form)


def find_student(input_form):
    id_student = find_student_page.main_student(input_form)
    timetable_json.main_student(id_student)


@app.route('/find', methods=["GET", "POST"])
def find():
    if request.method == 'POST':
        student = request.form.get('student')
        teacher = request.form.get('teacher')
        flag = 'flag' in request.form

        student_result = jsonify(student)
        find_student(student_result.json)
        teacher_result = jsonify(teacher)
        find_teacher(teacher_result.json)
        if one_teacher_table(str(flag)) is not None:
            return render_template('table.html')
        else:
            return render_template('index.html', student=student, teacher=teacher, flag=flag)


def one_teacher_table(flag):
    f = open('static/json/info_teacher.json', encoding='utf-8')
    data = json.load(f)
    res = data['teacher']
    if len(res) == 1:
        for i in res:
            if i['index']:
                result = i['index']
                timetable_json.main_teacher(result)
                free_time.main(flag)
                return result
    f.close()


def one_teacher():
    f = open('static/json/info_teacher.json', encoding='utf-8')
    data = json.load(f)
    res = data['teacher']
    for i in res:
        if i['index']:
            return i['index']
    f.close()


@app.route("/time", methods=["GET", "POST"])
def timetable():
    result = request.form.get('id')
    flag = request.form.get('flag')
    if result == "":
        result = one_teacher()
    timetable_json.main_teacher(result)
    free_time.main(flag)
    return render_template('table.html')


if __name__ == '__main__':
    app.run(port=5000)
