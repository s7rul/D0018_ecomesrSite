
from datetime import datetime
from flask import render_template
from HelloFlask import app
import pymysql
import pymysql.cursors

@app.route('/')
@app.route('/home')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")


    
    return render_template(
        "index.html",
        title = "WHISKYMASTER",
        content = " on " + formatted_now)


@app.route('/whisky')
def whisky():


    #The connection the the server.
    con = pymysql.connect(host='localhost',
        user='root',
        password='3306',
        db='whiskymaster',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            whiskyprod = []

            cur.execute('SELECT * FROM whisky')

            rows = cur.fetchall()

            for row in rows:
                #print(row['WhiskyName'])
                whiskyprod.append(row['WhiskyName'])

    finally:

        con.close()

    return render_template(
    "whisky.html",
    title = "Whisky Master",
    message = whiskyprod)
