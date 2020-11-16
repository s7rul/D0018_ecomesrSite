from datetime import datetime
from flask import render_template, request, redirect, make_response
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

                cur.execute("SELECT * FROM customers WHERE UserName=%s AND PassW=%s;", (str(form.userName.data), str(form.passW.data)))

                row = cur.fetchone()

                if row == None:
                    return "You done Goffed"
                    
                else:
                    return userPageLogin(row['CustomerID'])
                    #return redirect('/user/'+ row['CustomerID'])



        finally:
            con.close()
        
    return render_template(
    "login.html",
    form=form)




def userPageLogin(ID):
    #The connection the the server.
    con = getConnection()

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            cur.execute("SELECT * FROM customers WHERE CustomerID=%s;", (ID,))

            row = cur.fetchone()

    finally:

        con.close()

    ret = make_response(render_template(
    "userPage.html",
    title = "Whisky Master",
    customer = row))
    #set the cookie
    ret.set_cookie('userID', ID)
    return ret

@app.route('/user/')
def userPageCookie():
    ID = request.cookies.get('userID')

    if ID == None:
        return redirect('/login')
    else:
        return userPageLogin(ID)

@app.route('/user/<userID>')
def userPageURL(userID):


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
