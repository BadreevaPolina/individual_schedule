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
    return render_template('index.html')


@app.route('/id_student', methods=["GET", "POST"])
def student():
    result = jsonify(request.form.get("text"))
    print(result.json)
    return render_template('index.html')


@app.route("/time")
def timetable():
    return render_template('table.html')


if __name__ == '__main__':
    app.run(port=5000)
