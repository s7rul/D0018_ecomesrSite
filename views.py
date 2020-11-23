from datetime import datetime
from flask import render_template, request, redirect
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.sqlConnection import getConnection


import HelloFlask.users

import HelloFlask.whiskyInfo

import HelloFlask.admin


#A generic succsess page used for testing
@app.route('/succsess/<data>')
def succsess(data):
    return render_template("succsess.html", message=data)
