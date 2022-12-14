
import json

from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

import find_student_json
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
    return render_template('index.html')


def find_student(input_form):
    id_student = find_student_json.main_student(input_form)
    timetable_json.main_student(id_student)
    return render_template('index.html')


@app.route('/find', methods=["GET", "POST"])
def find():
    if request.method == 'POST':
        student = request.form.get('student')
        teacher = request.form.get('teacher')
        # if not student:
        #     flash('Группа студента не введена!')
        # elif not teacher:
        #     flash('ФИО преподавателя не введено!')
        # else:
        student_result = jsonify(student)
        find_student(student_result.json)
        teacher_result = jsonify(teacher)
        find_teacher(teacher_result.json)
    return render_template('index.html')


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
    if result == "":
        result = one_teacher()
    timetable_json.main_teacher(result)
    free_time.main()
    return render_template('table.html')


if __name__ == '__main__':
    app.run(port=5000)
