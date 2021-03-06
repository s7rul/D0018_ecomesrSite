from datetime import datetime
from flask import render_template, request, redirect
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.forms.AddForm import AddForm
from HelloFlask.sqlConnection import getConnection
from HelloFlask.purshese import addToBasket
from HelloFlask.users import addComment, rateWhisky, userValidLogin

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


            cur.execute('SELECT * FROM whisky WHERE Active = True;')

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
    #form = AddForm(request.form)
    if (request.method == 'POST'):

        if not userValidLogin():
            return redirect('/login', 303)

        print(request.form)

        comments = request.form

        field = (next(iter(request.form)))
        print(field)


        #End up here if comments.
        if field == 'Comments':

            if len(comments['Comments']) > 511:
                return "comment To long"

            if addComment(whiskyID, comments['Comments']):
                return redirect('/whisky/' + whiskyID)
            else:
                return redirect('/login')

        #End up here if Buy
        elif field == 'addToCart':
            count = int(request.form['addToCart'])
            print(count)

            if addToBasket(whiskyID, count):
                print("here")
                return redirect('/whisky/' + whiskyID)
            else:
                return redirect('/login')
        elif field == 'rate':
            if rateWhisky(whiskyID, comments['rate']):
                return redirect('/whisky/' + whiskyID)
            else:
                return redirect('/login')
        else:
            return 'wrong!!!!!'



    else:
        #The connection the the server.
        con = getConnection()

        # Try to connect to the server and find all values for
        # whisky tabel.
        try:

            with con.cursor() as cur:

                cur.execute("SELECT * FROM whisky WHERE WhiskyID=%s;", (str(whiskyID),))
                row = cur.fetchone()

                cur.execute("SELECT * FROM comments WHERE ProductNumber=%s;", (str(whiskyID),))
                comments = cur.fetchall()

                cur.execute("SELECT AVG(Grade) FROM grading WHERE ProductNumber = %s;", (whiskyID,))
                grade = cur.fetchone()


        finally:

            con.close()

        return render_template(
        "whiskypage.html",
        title = "Whisky Master",
        message = row,
        comments = comments,
        grade = grade)

