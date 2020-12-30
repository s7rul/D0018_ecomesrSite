from datetime import datetime
from flask import render_template, request, redirect, make_response
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.sqlConnection import getConnection
from HelloFlask.purshese import purchaseBasket

def getUsername():
    userID = request.cookies.get('userID')

    if userID == None:
        return None

    con = getConnection()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT UserName FROM customers WHERE CustomerID=%s;", (userID,))
            name = cur.fetchone()
            name = name['UserName']
    finally:
        con.close()

    return name



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

        finally:
            con.close()

        if row == None:
            return "You done Goffed"
              
        else:
            ret = make_response(redirect('/user/', 303))
            ret.set_cookie('userID', str(row['CustomerID']))
            return ret
        
    return render_template(
    "login.html",
    form=form)



@app.route('/user/')
def userPageCookie():
    ID = request.cookies.get('userID')

    if ID == None:
        return redirect('/login')

    con = getConnection()

    try:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM customers WHERE CustomerID=%s;", (ID,))
            row = cur.fetchone()

    finally:
        con.close()

    return render_template('userPage.html', customer = row)



@app.route('/basket', methods=['GET', 'POST'])
def basketPage():
    error = 'no'

    userID = request.cookies.get('userID')

    if userID==None:
        return redirect("/login")

    if request.method == 'POST':
        print("form: "+ str(request.form))
        field = (next(iter(request.form)))
        
        #buy basket
        if field == "buy":
            con = getConnection()
            basketID = None

            try:
                with con.cursor() as cur:
                    cur.execute("SELECT ID from Basket WHERE CustomerID = %s;", (userID,))
                    basketID = cur.fetchone()['ID']
                    print("basketID: " + str(basketID))
                con.commit()

            finally:
                con.close()

            if not purchaseBasket(userID, basketID):
                error = 'no purshese'
                
            

        #update basket
        else:
            print(request.form)
            qvant = request.form[field]
            print("ID " + field + "\nQ: " + qvant)
            if qvant == '' or int(qvant) < 0:
                return redirect('/basket')

            con = getConnection()

            if qvant == '0':
                try:
                    with con.cursor() as cur:
                        cur.execute("DELETE FROM BasketProduct WHERE ID = %s;", (field, ))
                    con.commit()

                finally:
                    con.close()
            else:
                try:
                    with con.cursor() as cur:
                        cur.execute("UPDATE BasketProduct SET Quantity=%s WHERE ID = %s;", (qvant, field))
                    con.commit()

                finally:
                    con.close()

            return redirect('/basket')



    #The connection the the server.
    con = getConnection()


    # Try to connect to the server and find all values for
    # whisky tabel.
    try:


        with con.cursor() as cur:
            cur.execute("SELECT * FROM (whisky INNER JOIN BasketProduct on whisky.WhiskyID=BasketProduct.ProductNumber) WHERE BasketID = (SELECT ID FROM Basket WHERE CustomerID=%s);", (userID,))
            row = cur.fetchall()

            cur.execute("SELECT SUM(Price * Quantity) FROM (whisky INNER JOIN BasketProduct on whisky.WhiskyID=BasketProduct.ProductNumber) WHERE BasketID = (SELECT ID FROM Basket WHERE CustomerID=%s);", (userID,))

            price = cur.fetchone()
            price = price['SUM(Price * Quantity)']



    finally:

        con.close()



    return render_template(
    "basket.html",
    title = "Whisky Master",
    basket = row,
    price = price,
    error = error)

@app.route('/register', methods=['GET', 'POST'])
def registerUser():

    if request.method == 'POST':
        print(request.form)
        form = request.form

        con = getConnection()

        try:
            with con.cursor() as cur:

                cur.execute("SELECT * FROM customers WHERE UserName=%s OR Mail=%s;", (form['UserName'], form['Mail']))
                rows = cur.fetchone()

                
                if rows == None:
                    cur.execute("SET @id = IF(EXISTS(SELECT CustomerID FROM customers), ((SELECT MAX(CustomerID) FROM customers) + 1), 0);")

                    cur.execute("""INSERT INTO customers(CustomerID, CorpName, UserName, PassW, Mail, PNumber, City, Address, ZipCode)
                        VALUES (@id, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (form['CorpName'], form['UserName'], form['PassW'], form['Mail'], form['PNumber'], form['City'], form['Address'], 'ZipCode'))
                    print("insert")
                        
                    con.commit()

                else:
                    con.close()
                    return "Username or Mail is taken"



                


        finally:
            con.close()

    return render_template("register.html")


def addComment(whiskyID, comment):

    userID = request.cookies.get('userID')

    if userID == None:
        return False

    con = getConnection()

    try:
        with con.cursor() as cur:
            cur.execute("SET @id = IF(EXISTS(SELECT ID FROM comments), ((SELECT MAX(ID) FROM comments) + 1), 0);")
            cur.execute("SET @username = (SELECT UserName from customers WHERE CustomerID = %s);", (userID,))
            cur.execute("INSERT INTO comments( ID, UserName, Comments, UserID, Productnumber) VALUES (@id, @username, %s, %s, %s);", (comment, userID, whiskyID))

            con.commit()

    finally:
        con.close()


    return True

def rateWhisky(whiskyID, grade):
    userID = request.cookies.get('userID')

    if userID == None:
        return False

    con = getConnection()

    try:
        with con.cursor() as cur:

            cur.execute("SELECT GradingID FROM grading WHERE UserID = %s AND ProductNumber = %s;", (userID, whiskyID))
            if cur.fetchone() == None:
                cur.execute("SET @id = IF(EXISTS(SELECT GradingID FROM grading), ((SELECT MAX(GradingID) FROM grading) + 1), 0);")
                cur.execute("INSERT INTO grading( GradingID, Grade, ProductNumber, UserID) VALUES (@id, %s, %s, %s);", (grade, whiskyID, userID))
            else:
                cur.execute("UPDATE grading SET Grade = %s WHERE ProductNumber = %s AND UserID = %s;", (grade, whiskyID, userID))

            con.commit()

    finally:
        con.close()


    return True






@app.route('/oders')
def oders():


    userID = request.cookies.get('userID')

    if userID == None:
        return redirect('/login')

    #The connection the the server.
    con = getConnection()
    # Try to connect to the server and find all values for
    # whisky tabel.


    try:

        with con.cursor() as cur:
            cur.execute("SELECT * from reserved WHERE CustomerID = %s;", (userID,))
            oders = cur.fetchall()


    finally:

        con.close()

    return render_template("oders.html",
                           oders = oders)


@app.route('/oders/<ID>')
def oder(ID):


    userID = request.cookies.get('userID')

    if userID == None:
        return redirect('/login')

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



    return render_template("oder.html",
                           whisky = rows,
                           price = price,
                           info=info)
