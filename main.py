"""main page"""
import json
import os
import logging
from datetime import timedelta
from urllib.parse import parse_qs, unquote_plus

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, session, url_for, jsonify
from flask_bootstrap import Bootstrap

import find_student_page
import find_teacher_json
import free_time
import timetable_json

app = Flask(__name__, static_url_path="/individual-schedule/static")
app.secret_key = os.urandom(30).hex()  # 'aCYmoeg6rRHI_ifsz04D8A'
app.permanent_session_lifetime = timedelta(days=3650)
app.config['JSON_AS_ASCII'] = False
bootstrap = Bootstrap(app)


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error="Ошибка. Страница не найдена.")


@app.errorhandler(500)
def timetable_error(error):
    return jsonify({"message": "Ошибка. На timetable что-то пошло не так."}), 500


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Ошибка. Попробуйте снова."}), 500


@app.errorhandler(500)
def internal_error_page(error):
    return render_template("error.html", error="Ошибка. Попробуйте снова.")


@app.route("/individual-schedule/")
def index():
    """main page"""
    return render_template("index.html", json_teachers="None", words_error="None")


def delete_comma(error, basic):
    """delete comma when returning input"""
    if error != "":
        error = error[: len(error) - 2]
    else:
        basic = basic[: len(basic) - 2]
    return error, basic


def find_teacher(input_form):
    """information about teachers"""
    try:
        teachers, teachers_error = find_teacher_json.main_teacher(input_form)
        if teachers is None:
            return None, None, ""
        teachers_error, teachers = delete_comma(teachers_error, teachers)
        return teachers, len(teachers[: len(teachers) - 2].split(",")), teachers_error
    except Exception as e:
        logging.exception(e)
        return None, None, ""


def edit_input_students(input_form):
    """edit input field for students"""
    try:
        students = input_form.strip().split(",")
        if len(students) == 1:
            students = input_form.split(" ")
        students = [i for i in students if i != ""]
        id_students, students_full, students_error = "", "", ""
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
                students_error = students_error + student.strip() + ", "
        return id_students, students_full, students_error
    except Exception as e:
        logging.exception(e)
        return "", "", ""


def find_student(input_form):
    """information about id student"""
    id_students, students_full, students_error = edit_input_students(input_form)
    timetable_json.main_student(id_students, students_full.split(","))
    students_error, students_full = delete_comma(students_error, students_full)
    return students_full, students_error


def get_info_teachers():
    """get information from a json"""
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data = json.load(file)
    json_teachers = str(data).replace("'", '"')
    if json_teachers == '{"teacher": []}':
        json_teachers = "None"
    return json_teachers


def get_info_json_file(filename):
    with open(filename, encoding="utf8") as file:
        data = json.load(file)
    json_file = str(data).replace("'", '"')
    return json_file


def get_info_incorrect_data():
    """get information from a json"""
    result = ""
    with open("static/json/incorrect_data.json", encoding="utf8") as file:
        data = json.load(file)
    try:
        for i in data:
            for j in data[i]:
                result = result + str(j) + "\n"
        if result == "" or result == " ":
            return "None"
        else:
            return result[: len(result) - 1]
    except Exception as e:
        logging.exception(e)
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


def timetable_work():
    cookie = {"_culture": "ru", "value": "ru"}
    url_page = "https://timetable.spbu.ru/"
    url_ru = requests.get(url_page, cookies=cookie, timeout=15).text
    html_person = BeautifulSoup(url_ru, "lxml")
    if (
        html_person.find("h2").text is not None
        and html_person.find("h2").text == "Ошибка "
    ):
        return False
    return True


def one_zero_teacher_table(flag, count_teacher):
    """if found one teacher, show result page"""
    with open("static/json/info_teacher.json", encoding="utf8") as file:
        data_t = json.load(file)
    with open("static/json/student.json", encoding="utf8") as file:
        data_s = json.load(file)
    if len(data_t["teacher"]) == 0 and len(data_s) >= 1:
        timetable_json.main_teacher("", [""])
        free_time.main(flag)
        return "ok"
    indices, teachers = "", []
    if len(data_t["teacher"]) == count_teacher:
        for i in data_t["teacher"]:
            if i["index"]:
                indices = indices + i["index"] + ","
                teachers = teachers + [i["full_name"]]
        timetable_json.main_teacher(indices, teachers)
        free_time.main(flag)
        return flag
    return None


def name_teachers(str_teachers):
    """find selected teachers"""
    str_teachers = str_teachers[: len(str_teachers) - 2].split(", ")
    teachers = []
    for _, teacher in enumerate(str_teachers):
        teachers = teachers + [teacher]
    return teachers


def get_info_schedule():
    incorrect_data = get_info_incorrect_data()
    timetable_unchanged_json = get_info_json_file(
        "static/json/timetable_unchanged.json"
    )
    answer_json = get_info_json_file("static/json/answer.json")
    return incorrect_data, timetable_unchanged_json, answer_json


@app.route("/individual-schedule/timetable", methods=["GET", "POST"])
def timetable():
    """show result page"""
    if request.method == "GET":
        incorrect_data, timetable_unchanged_json, answer_json = get_info_schedule()
        return render_template(
            "table.html",
            incorrect_data=incorrect_data,
            json_teachers="None",
            timetable_unchanged_json=timetable_unchanged_json,
            answer_json=answer_json,
        )
    if request.method == "POST":
        try:
            index_teachers = request.form.get("index_teachers")
            teachers = name_teachers(request.form.get("teachers"))
            words_error = request.form.get("words_error")
            timetable_json.main_teacher(index_teachers, teachers)
            free_time.main(session.get("flag_place", default=False))
        except Exception as e:
            logging.exception(e)
            return internal_error_page(500)
        incorrect_data, timetable_unchanged_json, answer_json = get_info_schedule()
        return render_template(
            "table.html",
            incorrect_data=incorrect_data,
            timetable_unchanged_json=timetable_unchanged_json,
            answer_json=answer_json,
            json_teachers="None",
            words_error=words_error,
        )


@app.route("/individual-schedule/find", methods=["GET", "POST"])
def find():
    """show find teachers or result page"""
    if request.method == "POST":
        data = request.data.decode('utf-8')
        params = parse_qs(data)
        student = unquote_plus(params.get('student', [''])[0])
        teacher = unquote_plus(params.get('teacher', [''])[0])
        flag_place = params.get('flag_place')[0]
        if flag_place is None:
            flag_place = "False"
        session["flag_place"] = str(flag_place)
        session["student"], session["teacher"] = student, teacher
        student, student_error = find_student(student)
        teacher, count_teacher, teacher_error = find_teacher(teacher)
        if student is None or teacher is None:
            return internal_error_page(505)
        if student == "" and teacher == "":
            if not timetable_work():
                return timetable_error(505)

        json_teachers = get_info_teachers()
        words_error = write_words_error(student_error, teacher_error)
        check = one_zero_teacher_table(session["flag_place"], count_teacher)
        if check is not None and words_error == "None":
            return jsonify({"redirect": url_for("timetable")})
        else:
            return jsonify(
                {
                    "count_teacher": count_teacher,
                    "json_teachers": json_teachers,
                    "words_error": words_error,
                }
            )


if __name__ == "__main__":
    log_file_path = os.environ.get("LOG_FILE")
    if log_file_path is None:
        print("LOG_FILE not specified")
        exit(1)
    print(f"LOG_FILE specified: {log_file_path}")
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file_path,
        format="%(levelname)s (%(asctime)s): %(message)s "
        "(Line: %(lineno)d) [%(filename)s]",
        datefmt="%d/%m/%Y %I:%M:%S",
        encoding="utf-8",
        filemode="w",
    )
    app.run(port=5000, host="0.0.0.0")
