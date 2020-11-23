
from datetime import datetime
from flask import render_template, request, redirect, make_response
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.sqlConnection import getConnection





@app.route('/admin/login', methods=['GET', 'POST'])
def loginAdmin():
    
    form = LoginForm(request.form)


    if (request.method == 'POST'):

        con = getConnection()
        # Try to connect to the server and find all values for
        # whisky tabel.
        try:
            with con.cursor() as cur:

                cur.execute("SELECT * FROM admins WHERE UserName=%s AND PassW=%s;", (str(form.userName.data), str(form.passW.data)))

                row = cur.fetchone()

                if row == None:
                    return "You done Goffed"
                    
                else:
                    return "Foudn the User"




        finally:
            con.close()
        
    return render_template(
    "adminLogin.html",
    form=form)


def userPageLoginAdmin(ID):
    #The connection the the server.
    con = getConnection()

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            cur.execute("SELECT * FROM admins WHERE CustomerID=%s;", (ID,))

            row = cur.fetchone()

    finally:

        con.close()

    ret = make_response(render_template(
    "admin.html",
    title = "Whisky Master",
    customer = row))
    #set the cookie
    ret.set_cookie('userID', ID)
    return ret

@app.route('/admin', methods=['GET', 'POST'])
def admin():



    if request.method == 'POST':
        modID = (next(iter(request.form)))
        qvant = request.form[modID]
        if qvant == '' or int(qvant) < 0:
            return redirect('/admin')

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

@app.route('/admin/editwhisky/<id>', methods=['GET', 'POST'])
def editWhiskuPage(id):
    if request.method == 'POST':
        print(request.form)

    con = getConnection()

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM whisky WHERE WhiskyID=%s;", (str(id),))
            whisky = cur.fetchone()
    finally:
        con.close()

    return render_template("editwhisky.html", whisky=whisky)