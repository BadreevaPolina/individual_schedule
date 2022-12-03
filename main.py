import sys

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000)
