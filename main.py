"""main page"""
import json

from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

import find_student_page
import find_teacher_json
import free_time
import timetable_json

app = Flask(__name__, static_url_path="/individual-schedule/static")

bootstrap = Bootstrap(app)


@app.route("/individual-schedule/")
def index():
    """main page"""
    return render_template('index.html', json_teachers="None", words_error="None")


def delete_comma(error, basic):
    """delete comma when returning input"""
    if error != "":
        error = error[:len(error) - 1]
    else:
        basic = basic[:len(basic) - 1]
    return error, basic


def find_teacher(input_form):
    """information about teachers"""
    teachers, teachers_error = find_teacher_json.main_teacher(input_form)
    if teachers is None:
        return None, None, ""
    teachers_error, teachers = delete_comma(teachers_error, teachers)
    return teachers, len(teachers[:len(teachers) - 1].split(",")), teachers_error


def find_student(input_form):
    """information about id student"""
    students = input_form.split(",")
    if len(students) == 1:
        students = input_form.split(" ")
    id_students = ""
    students_full = ""
    students_error = ""
    for student in students:
        student_properly = student.strip().upper()
        student_properly = student_properly.replace("-ММ", "-мм")
        if "-мм" not in student_properly:
            student_properly += "-мм"
        if "." not in student_properly:
            student_properly = student_properly[:2] + "." + student_properly[2:]
        id_student = find_student_page.main_student(student_properly)
        if id_student is not None and id_student != "":
            id_students = id_students + id_student + ","
            students_full = students_full + student_properly + ", "
        elif id_student == "":
            students_error = students_error + student + ", "
    students_full = students_full[:len(students_full) - 1]
    timetable_json.main_student(id_students, students_full.split(","))
    students_error, students_full = delete_comma(students_error, students_full)
    return students_full, students_error[:len(students_error) - 1]


def get_info_teachers():
    """get information from a json"""
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data = json.load(file)
    return str(data).replace("\'", "\"")


def get_info_answer():
    """get information from a json"""
    with open("static/json/answer.json", encoding="utf8") as file:
        data = json.load(file)
    if str(data) == "[]":
        return "None"
    return "ok"


def get_info_incorrect_data():
    """get information from a json"""
    result = ""
    with open("static/json/incorrect_data.json", encoding="utf8") as file:
        data = json.load(file)
    try:
        for i in data:
            for j in data[i]:
                result = result + str(j) + '\n'
        return result[:len(result)-1]
    except (AttributeError, IndexError):
        return "None"


def write_words_error(student_error, teacher_error):
    """combine words with mistake"""
    if student_error != "" and teacher_error != "":
        words_error = student_error + ", " + teacher_error
    else:
        words_error = student_error + teacher_error
    if words_error == "":
        words_error = "None"
    return words_error


@app.route('/individual-schedule/find', methods=["GET", "POST"])
def find():
    """main page with information about teachers or return result timetable"""
    if request.method == 'POST':
        student = request.form.get('student')
        teacher = request.form.get('teacher')
        flag_place = 'flag_place' in request.form
        student_result = jsonify(student)
        student, student_error = find_student(student_result.json)
        teacher_result = jsonify(teacher)
        teacher, count_teacher, teacher_error = find_teacher(teacher_result.json)
        if student is None or teacher is None:
            return render_template('error.html')
        json_teachers = get_info_teachers()
        words_error = write_words_error(student_error, teacher_error)
        if one_zero_teacher_table(str(flag_place), count_teacher) is not None \
                and words_error == "None":
            incorrect_data = get_info_incorrect_data()
            return render_template('table.html', student=student, teacher=teacher,
                                   incorrect_data=incorrect_data, json_teachers="None",
                                   words_error=words_error, answer=get_info_answer())
        return render_template('index.html', student=student + student_error,
                               teacher=teacher + teacher_error, flag_place=flag_place,
                               checkbox_checked="checked" if flag_place else "",
                               count_teacher=count_teacher, json_teachers=json_teachers,
                               words_error=words_error, answer=get_info_answer())
    return render_template('index.html', json_teachers="None", words_error="None")


def one_zero_teacher_table(flag, count_teacher):
    """if found one teacher, show result page"""
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data_t = json.load(file)
    with open("static/json/student.json", encoding="utf8") as file:
        data_s = json.load(file)
    if len(data_t['teacher']) == 0 and len(data_s) > 1:
        timetable_json.main_teacher("", [""])
        free_time.main(flag)
        return "ok"
    indexs = ""
    teachers = []
    if len(data_t['teacher']) == count_teacher:
        for i in data_t['teacher']:
            if i['index']:
                indexs = indexs + i['index'] + ","
                teachers = teachers + [i['full_name']]
        timetable_json.main_teacher(indexs, teachers)
        free_time.main(flag)
        return flag
    return None


def name_teachers(index_teachers):
    """find selected teachers"""
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data_t = json.load(file)
    try:
        index_teachers = index_teachers.split(", ")
        teachers = []
        for _, index_teacher in enumerate(index_teachers):
            for i in data_t['teacher']:
                if i['index'] == index_teacher:
                    teachers = teachers + [i['full_name']]
        return teachers
    except AttributeError:
        return ""


@app.route("/individual-schedule/time", methods=["GET", "POST"])
def timetable():
    """show result page"""
    flag_place = request.form.get('flag_place')
    index_teachers = request.form.get('index_teachers')
    teachers = name_teachers(index_teachers)
    timetable_json.main_teacher(index_teachers, teachers)
    try:
        free_time.main(str(flag_place))
    except json.decoder.JSONDecodeError:
        return render_template('error.html')
    student = request.form.get('student')
    teacher = request.form.get('teacher')
    words_error = request.form.get('words_error')
    incorrect_data = get_info_incorrect_data()
    return render_template('table.html', student=student, teacher=teacher, json_teachers="None",
                           words_error=words_error, incorrect_data=incorrect_data, answer=get_info_answer())


@app.route("/individual-schedule/time-find", methods=["GET", "POST"])
def timetable_find():
    """show find teachers or result page"""
    if request.method == 'POST':
        student = request.form.get('student')
        teacher = request.form.get('teacher')

        student_result = jsonify(student)
        student, student_error = find_student(student_result.json)
        teacher_result = jsonify(teacher)
        teacher, count_teacher, teacher_error = find_teacher(teacher_result.json)
        if student is None or teacher is None:
            return render_template('error.html')
        json_teachers = get_info_teachers()
        if json_teachers == "{\"teacher\": []}":
            json_teachers = "None"
        words_error = write_words_error(student_error, teacher_error)
        if one_zero_teacher_table("False", count_teacher) is not None and words_error == "None":
            incorrect_data = get_info_incorrect_data()
            return render_template('table.html', student=student, teacher=teacher,
                                   words_error=words_error, incorrect_data=incorrect_data,
                                   json_teachers="None", answer=get_info_answer())
        return render_template('table.html', student=student + student_error,
                               teacher=teacher + teacher_error,
                               count_teacher=count_teacher, json_teachers=json_teachers,
                               words_error=words_error, incorrect_data="None", answer=get_info_answer())
    return render_template('table.html')


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
