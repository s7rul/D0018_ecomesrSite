
from datetime import datetime
from flask import render_template, request, redirect, make_response
from HelloFlask import app
import pymysql
import pymysql.cursors
import os
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.sqlConnection import getConnection

app.config["IMAGE_UPLOADS"] = "HelloFlask/static"



@app.route('/admin/orders', methods=['GET', 'POST'])
def adminOrders():
    #The connection the the server.
    con = getConnection()
    # Try to connect to the server and find all values for
    # whisky tabel.

    try:
        with con.cursor() as cur:
            cur.execute("SELECT * from reserved;")
            oders = cur.fetchall()


    finally:

        con.close()

    return render_template("adminOrders.html",
                           oders = oders)

@app.route('/admin/order/<ID>', methods=['GET', 'POST'])
def adminOrder(ID):




    #The connection the the server.
    con = getConnection()
    # Try to connect to the server and find all values for
    # whisky tabel.

    try:
        with con.cursor() as cur:
            cur.execute("SELECT whisky.WhiskyID, whisky.WhiskyName, reservedProduct.Price, reservedProduct.Quantity FROM (whisky INNER JOIN reservedProduct on whisky.WhiskyID=reservedProduct.ProductNumber) WHERE ReservedID = %s;", (ID,))
            rows = cur.fetchall()

            cur.execute("SELECT SUM(Price * Quantity) FROM reservedProduct WHERE ReservedID = %s;", (ID,))

            price = cur.fetchone()
            price = price['SUM(Price * Quantity)']

            cur.execute("""SELECT
                customers.CustomerID,
                customers.CorpName,
                customers.UserName,
                customers.Mail,
                customers.PNumber,
                reserved.ReservedID,
                reserved.City,
                reserved.Adress,
                reserved.ZipCode,
                reserved.ReservedStatus
                FROM
                (reserved INNER JOIN customers ON
                reserved.CustomerID = customers.CustomerID)
                WHERE
                reserved.ReservedID = %s""",
                (ID,))
            info = cur.fetchone()


    finally:

        con.close()

    print(rows)



    return render_template("adminOrder.html",
                           whisky = rows,
                           price = price,
                           info = info)

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
        return redirect('/admin/login', 303)

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



@app.route('/admin/editwhisky/<wid>', methods=['GET', 'POST'])
def editWhiskuPage(wid):
    if request.method == 'POST':
        field = next(iter(request.form))
        value = request.form[field]

        if value == "":
            return redirect('/admin/editwhisky/' + str(wid))

        if field == "dont":
            con = getConnection()
            try:
                with con.cursor() as cur:
                    cur.execute("UPDATE whisky SET Active = False WHERE WhiskyID = %s;",(wid, ))
                    cur.execute("DELETE FROM BasketProduct WHERE ProductNumber = %s;", (wid, ))
                con.commit()
            finally:
                con.close()
            return redirect('/admin/editwhisky/' + str(wid))

        if field == "do":
            con = getConnection()
            try:
                with con.cursor() as cur:
                    cur.execute("UPDATE whisky SET Active = True WHERE WhiskyID = %s;",(wid, ))
                con.commit()
            finally:
                con.close()
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

            cur.execute("SELECT * FROM comments WHERE ProductNumber=%s;", (str(wid),))
            comments = cur.fetchall()

            cur.execute("SELECT AVG(Grade) FROM grading WHERE ProductNumber = %s;", (wid,))
            grade = cur.fetchone()

    finally:
        con.close()

    return render_template("editwhisky.html", 
                           whisky=whisky,
                           comments = comments,
                           grade = grade)




@app.route("/admin/uploadImage", methods=["GET", "POST"])
def upload_image():

    print(os.getcwd())

    if request.method == "POST":

        if request.files:

            image = request.files["image"]


            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))


            #Check if the name was a number.
            try:
                int(image.filename.split(".")[0])

            except:
                return redirect(request.url)


            con = getConnection()
            try:
                with con.cursor() as cur:
                    cur.execute(("UPDATE whisky SET Picture=True WHERE WhiskyID = %s;"),(image.filename.split(".")[0],))
                con.commit()
            finally:
                con.close()


            return redirect(request.url)

    return render_template("uploadImage.html")




@app.route('/admin/addwhisky', methods=['GET', 'POST'])
def addWhiskyPage():
    if request.method == 'POST':
        print(request.form)
        form = request.form

        con = getConnection()
        try:
            with con.cursor() as cur:
                cur.execute("SET @id = IF(EXISTS(SELECT WhiskyID FROM whisky), ((SELECT MAX(WhiskyID) FROM whisky) + 1), 0);")
                if form['Region'] != "":
                    cur.execute("""INSERT INTO whisky(WhiskyID, WhiskyName, Price, StorageLeft, Nation, Distillery, Region, Alohol, Picture, Active)
                        VALUES (@id, %s, %s, %s, %s, %s, %s, %s, %s, True)""",
                        (form['WhiskyName'], form['Price'], form['StorageLeft'], form['Nation'], form['Distillery'], form['Region'], form['Alohol'], '0'))
                else:
                    cur.execute("""INSERT INTO whisky(WhiskyID, WhiskyName, Price, StorageLeft, Nation, Distillery, Alohol, Picture, Active)
                        VALUES (@id, %s, %s, %s, %s, %s, %s, %s, True)""",
                        (form['WhiskyName'], form['Price'], form['StorageLeft'], form['Nation'], form['Distillery'], form['Alohol'], '0'))
            con.commit()
        finally:
            con.close()

    return render_template("addWhisky.html")

