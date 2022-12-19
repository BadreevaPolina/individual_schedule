
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
import json

import find_teacher_json


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/find_teacher', methods=["GET", "POST"])
def teacher():
    result = jsonify(request.form.get("text"))
    input_form = result.json
    print(input_form)
    find_teacher_json.main_teacher(input_form)
    return render_template('index.html'), input_form


@app.route('/id_student', methods=["GET", "POST"])
def student():
    result = jsonify(request.form.get("text"))
    print(result.json)
    return render_template('index.html')


@app.route("/time", methods=["GET", "POST"])
def timetable():
    return render_template('table.html')


if __name__ == '__main__':
    app.run(port=5000)
