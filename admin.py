
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
        row = None

        try:
            with con.cursor() as cur:

                cur.execute("SELECT * FROM admins WHERE UserName=%s AND PassW=%s;", (str(form.userName.data), str(form.passW.data)))

                row = cur.fetchone()


        finally:
            con.close()

        id = row['ID']

        if row == None:
            return "You done Goffed"
                    
        else:
            return userPageLoginAdmin(row['ID'])
        

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

            cur.execute('SELECT * FROM whisky')

            rows = cur.fetchall()

    finally:

        con.close()

    ret = make_response(render_template(
    "adminPage.html",
    title = "Whisky Master",
    inventory = rows))
    #set the cookie
    ret.set_cookie('adminID', ID)
    return ret


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    adminID = request.cookies.get('adminID')

    if adminID == None:
        return redirect('/admin/login')

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


"""def editWhiskyParameter(field, value):

    con = getConnection()
    if field == 'WhiskyID':
    elif field == 'WhiskyName':
        print("t")
    elif field == 'Price':
    elif field == 'Nation':
    elif field == 'StorageLeft':
    elif field == 'StorageLeft':
    Nation		VARCHAR(255),
    Distillery	VARCHAR(255),
    Region		VARCHAR(255),
    Alohol		VARCHAR(10)		NOT NULL,
    Sold		int,
    
    #Placeholder
    Picture 	VARCHAR(255),
    try:
        with con.cursor() as cur:
            cur.execute("UPDATE whisky SET %s=%s WHERE WhiskyID = %s;", (value, id))
            con.commit()
    finally:
        con.close()"""


@app.route('/admin/editwhisky/<wid>', methods=['GET', 'POST'])
def editWhiskuPage(wid):
    if request.method == 'POST':
        field = next(iter(request.form))
        value = request.form[field]

        if value == "":
            return redirect('/admin/editwhisky/' + str(wid))

        con = getConnection()
        try:
            with con.cursor() as cur:
                cur.execute(("UPDATE whisky SET " + field + "=%s WHERE WhiskyID = %s;"),(value, wid))
                con.commit()
        finally:
            con.close()


    con = getConnection()

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM whisky WHERE WhiskyID=%s;", (str(wid),))
            whisky = cur.fetchone()
    finally:
        con.close()

    return render_template("editwhisky.html", whisky=whisky)
