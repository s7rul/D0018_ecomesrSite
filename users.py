from datetime import datetime
from flask import render_template, request, redirect
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.sqlConnection import getConnection


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm(request.form)


    if (request.method == 'POST'):

        con = getConnection()
        # Try to connect to the server and find all values for
        # whisky tabel.
        try:
            with con.cursor() as cur:

                cur.execute("SELECT * FROM customers WHERE UserName=%s;", (str(form.userName.data),))

                row = cur.fetchone()

                if row == None:
                    return "You done Goffed"
                    
                else:
                    return redirect('/user/'+ row['CustomerID'])



        finally:
            con.close()
        
    return render_template(
    "login.html",
    form=form)

@app.route('/user/<userID>')
def userPage(userID):


    #The connection the the server.
    con = getConnection()

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            cur.execute("SELECT * FROM customers WHERE CustomerID=%s;", (userID,))


            row = cur.fetchone()


    finally:

        con.close()

    return render_template(
    "userPage.html",
    title = "Whisky Master",
    customer = row)
