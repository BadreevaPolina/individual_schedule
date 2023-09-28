"""main page"""
import os
import logging
from datetime import timedelta
from urllib.parse import parse_qs, unquote_plus

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, session, url_for, jsonify
from flask_bootstrap import Bootstrap

import find_student_page
import teacher_info_manager
import free_time_manager
import timetable_manager

app = Flask(__name__, static_url_path="/individual-schedule/static")
app.secret_key = "aCYmoeg6rRHI_ifsz04D8A"
app.permanent_session_lifetime = timedelta(days=3650)
app.config["JSON_AS_ASCII"] = False
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


def find_teacher(input_form, info_teacher_instance):
    """information about teachers"""
    try:
        teachers, teachers_error, info_teacher = info_teacher_instance.main_teacher(
            input_form
        )
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


def find_student(input_form, count_weeks=4):
    """information about id student"""
    id_students, students_full, students_error = edit_input_students(input_form)
    session["id_students"] = (id_students, students_full.split(","))
    students_error, students_full = delete_comma(students_error, students_full)
    return students_full, students_error


def get_info_teachers(info_teacher):
    """get information from a json"""
    json_teachers = str(info_teacher.info_teacher).replace("'", '"')
    if json_teachers == '{"teacher": []}':
        json_teachers = "None"
    return json_teachers


def get_info_incorrect_data(incorrect_time):
    """get information from a json"""
    try:
        result = "\n".join(str(j) for i in incorrect_time for j in incorrect_time[i])
        return result if result.strip() else "None"
    except Exception as e:
        logging.exception(e)
        return "None"


def write_words_error(student_error, teacher_error):
    """combine words with mistake"""
    words_error = ", ".join(filter(None, [student_error, teacher_error]))
    return words_error if words_error else "None"


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


def one_zero_teacher_table(count_teacher, info_teacher):
    if not info_teacher["teacher"] and len(session["id_students"][0]) >= 1:
        session["id_teachers"] = ("", [])
        return "ok"

    indices, teachers = [], []
    for teacher in info_teacher["teacher"]:
        if teacher["index"]:
            indices.append(teacher["index"])
            teachers.append(teacher["full_name"])

    if len(teachers) == count_teacher:
        session["id_teachers"] = (",".join(indices), teachers)
        return "ok"

    return None


def name_teachers(str_teachers):
    """find selected teachers"""
    str_teachers = str_teachers[: len(str_teachers) - 2].split(", ")
    teachers = []
    for _, teacher in enumerate(str_teachers):
        teachers = teachers + [teacher]
    return teachers


def get_info_schedule(count_weeks=4):
    timetable_instance = timetable_manager.TimetableManager()
    free_time_instance = free_time_manager.FreeTimeManager()
    timetable_instance.main_student(
        session["id_students"][0], session["id_students"][1], count_weeks
    )
    timetable_instance.main_teacher(
        session["id_teachers"][0], session["id_teachers"][1], count_weeks
    )
    free_time_instance.main(session["flag_place"], timetable_instance.timetable)

    incorrect_data = get_info_incorrect_data(timetable_instance.incorrect_time)
    timetable_unchanged_result = str(
        free_time_instance.timetable_unchanged_list
    ).replace("'", '"')
    answer_result = str(free_time_instance.answer_list).replace("'", '"')
    return incorrect_data, timetable_unchanged_result, answer_result


def delete_another_teachers(index_teachers, info_teacher_instance):
    desired_indexes = index_teachers.split(", ")
    filtered_teachers = [
        teacher
        for teacher in info_teacher_instance.info_teacher["teacher"]
        if teacher["index"] in desired_indexes
    ]
    info_teacher_instance.info_teacher["teacher"] = filtered_teachers


@app.route("/individual-schedule/timetable_4_month", methods=["GET", "POST"])
def timetable_4_month():
    if request.method == "POST":
        return jsonify({"redirect": url_for("timetable", count_weeks=16)})


@app.route("/individual-schedule/timetable", methods=["GET", "POST"])
def timetable():
    """show result page"""
    if request.method == "GET":
        count_weeks = int(request.args.get("count_weeks"))
        incorrect_data, timetable_unchanged_json, answer_json = get_info_schedule(
            count_weeks
        )
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
            session["id_teachers"] = (index_teachers, teachers)
            incorrect_data, timetable_unchanged_json, answer_json = get_info_schedule()
        except Exception as e:
            logging.exception(e)
            return internal_error_page(500)
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
        data = request.data.decode("utf-8")
        params = parse_qs(data)
        student = unquote_plus(params.get("student", [""])[0])
        teacher = unquote_plus(params.get("teacher", [""])[0])
        flag_place = params.get("flag_place")[0]

        session["flag_place"] = str(flag_place)
        session["student"], session["teacher"] = student, teacher

        info_teacher_instance = teacher_info_manager.TeacherInfoManager()
        student, student_error = find_student(student)
        teacher, count_teacher, teacher_error = find_teacher(
            teacher, info_teacher_instance
        )

        if student is None or teacher is None:
            return internal_error_page(505)
        if student == "" and teacher == "":
            if not timetable_work():
                return timetable_error(505)

        json_teachers = get_info_teachers(info_teacher_instance)
        words_error = write_words_error(student_error, teacher_error)
        check = one_zero_teacher_table(
            count_teacher, info_teacher_instance.info_teacher
        )

        if check is not None and words_error == "None":
            return jsonify({"redirect": url_for("timetable", count_weeks=4)})
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
