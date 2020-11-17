from datetime import datetime
from flask import render_template, request, redirect
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.sqlConnection import getConnection

@app.route('/')
@app.route('/home')
def home():

    #Adds time and date.
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")



    #Returns the HTML page with the set info.
    return render_template(
        "index.html",
        title = "WHISKYMASTER",
        content = " on " + formatted_now)


@app.route('/whisky')
def whisky():


    #The connection the the server.
    con = getConnection()
    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            whiskyNumber = []
            whiskyprod = []


            cur.execute('SELECT * FROM whisky')

            rows = cur.fetchall()

            for row in rows:
                whiskyNumber.append(row['WhiskyID'])
                whiskyprod.append(row['WhiskyName'])


    finally:

        con.close()

    return render_template(
    "whisky.html",
    title = "Whisky Master",
    message = whiskyprod,
    whiskyID = whiskyNumber)

@app.route('/whisky/<whiskyID>')
def whiskypage(whiskyID):


    #The connection the the server.
    con = getConnection()

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            cur.execute("SELECT * FROM whisky WHERE WhiskyID=%s;", (str(whiskyID),))


            row = cur.fetchone()


    finally:

        con.close()

    return render_template(
    "whiskypage.html",
    title = "Whisky Master",
    message = row)

@app.route('/admin')
def admin():


    #The connection the the server.
    con = getConnection()
    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            whiskyNumber = []
            whiskyprod = []
            storageLeft = []

            cur.execute('SELECT * FROM whisky')

            rows = cur.fetchall()

            for row in rows:
                whiskyNumber.append(row['WhiskyID'])
                whiskyprod.append(row['WhiskyName'])
                storageLeft.append(row['StorageLeft'])


    finally:

        con.close()

    return render_template(
    "adminPage.html",
    title = "Whisky Master",
    message = whiskyprod,
    whiskyID = whiskyNumber,
    storage = storageLeft)
