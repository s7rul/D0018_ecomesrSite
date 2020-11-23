from datetime import datetime
from flask import render_template, request, redirect
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.forms.AddForm import AddForm
from HelloFlask.sqlConnection import getConnection
from HelloFlask.purshese import addToBasket

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

@app.route('/whisky/<whiskyID>', methods=['GET', 'POST'])
def whiskypage(whiskyID):
    form = AddForm(request.form)
    if (request.method == 'POST'):
        try:
            count = int(form.addNumber.data)
        except:
            return "Wrong input"

        if addToBasket(whiskyID, count):
            return redirect('/whisky/' + whiskyID)
        else:
            return redirect('/login')
    else:
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
        message = row,
        form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():



    if request.method == 'POST':
        modID = (next(iter(request.form)))
        qvant = request.form[modID]
        if qvant == '' or int(qvant) < 0:
            return redirect('/basket')

        con = getConnection()

        try:
            with con.cursor() as cur:
                cur.execute("UPDATE whisky SET StorageLeft=%s WHERE WhiskyID = %s;", (qvant, modID))
                con.commit()

        finally:
            con.close()

        return redirect('/admin')




    #The connection the the server.
    con = getConnection()
    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        #Just want to fetch all the inventory.
        with con.cursor() as cur:

            cur.execute('SELECT * FROM whisky')

            rows = cur.fetchall()



    finally:

        con.close()

    return render_template(
    "adminPage.html",
    title = "Whisky Master",
    inventory = rows)
