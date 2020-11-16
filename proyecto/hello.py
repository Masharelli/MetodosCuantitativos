from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
   return render_template("llaves.html")

@app.route('/en-vivo')
def method_name():
   return render_template("envivo.html")
