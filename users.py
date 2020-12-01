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
            return userPageLogin(row['CustomerID'])
        
    return render_template(
    "login.html",
    form=form)




def userPageLogin(ID):
    #The connection the the server.
    con = getConnection()

    print(ID)

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
    #set the cookie Can only handel Strings.
    ID = str(ID)
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


@app.route('/basket', methods=['GET', 'POST'])
def basketPage():

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

            purchaseBasket(userID, basketID)
            

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

            cur.execute(" create temporary table basketTmp(SELECT * FROM BasketProduct WHERE BasketID IN (SELECT ID FROM Basket WHERE CustomerID=%s));", (userID,))
            cur.execute("select * from whisky inner join basketTmp on whisky.WhiskyID=basketTmp.ProductNumber;")

            row = cur.fetchall()

            cur.execute("create temporary table basketPrice(SELECT * FROM whisky inner join basketTmp on  whisky.WhiskyID=basketTmp.ProductNumber);")
            cur.execute("SELECT SUM(Price * Quantity) FROM basketPrice;")

            price = cur.fetchone()
            price = price['SUM(Price * Quantity)']



    finally:

        con.close()



    return render_template(
    "basket.html",
    title = "Whisky Master",
    basket = row,
    price = price)

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
