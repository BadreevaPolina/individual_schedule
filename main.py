import os
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
import json


app = Flask(__name__)
bootstrap = Bootstrap(app)

input_form = ""


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/find_teacher', methods=["GET", "POST"])
def teacher():
    result = jsonify(request.form.get("text"))
    input_form = result.json
    os.system('find_teacher_json.py')
    return render_template('index.html')


@app.route('/id_student', methods=["GET", "POST"])
def student():
    result = jsonify(request.form.get("text"))
    os.system('find_student_json.py')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000)
