from flask import render_template, request, redirect
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm

def getConnection():
    return pymysql.connect(host='localhost',
        user='whiskymaster',
        password='whisky',
        db='whiskymaster',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
