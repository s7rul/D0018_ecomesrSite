
from datetime import datetime
from flask import render_template, request, redirect
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm


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
    con = pymysql.connect(host='localhost',
        user='whiskymaster',
        password='whisky',
        db='whiskymaster',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            whiskyNumber = []
            whiskyprod = []


            cur.execute('SELECT * FROM WHISKY')

            rows = cur.fetchall()

            for row in rows:
                #print(row['WhiskyName'])
                #print(row['WhiskyID'])
                whiskyNumber.append(row['WhiskyID'])
                whiskyprod.append(row['WhiskyName'])


    finally:

        con.close()

    return render_template(
    "whisky.html",
    title = "Whisky Master",
    message = whiskyprod,
    whiskyID = whiskyNumber)

@app.route('/whisky/<whiskyID>')
def whiskypage(whiskyID):


    #The connection the the server.
    con = pymysql.connect(host='localhost',
        user='whiskymaster',
        password='whisky',
        db='whiskymaster',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    # Try to connect to the server and find all values for
    # whisky tabel.
    try:

        with con.cursor() as cur:

            name = ""

            

            cur.execute("SELECT * FROM WHISKY WHERE WhiskyID=%s;", (str(whiskyID),))


            row = cur.fetchone()


#            cur.execute("UPDATE whiskymaster.Whisky SET StorageLeft=120 WHERE WhiskyID='1'")

            
#            con.commit()
            



            #name = rows['WhiskyName']



    finally:

        con.close()

    return render_template(
    "whiskypage.html",
    title = "Whisky Master",
    message = row)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm(request.form)


    if (request.method == 'POST'):


#        print(form.passW.data)
#        return redirect('/whisky/1')

        con = pymysql.connect(host='localhost',
            user='whiskymaster',
            password='whisky',
            db='whiskymaster',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

        # Try to connect to the server and find all values for
        # whisky tabel.
        try:
            with con.cursor() as cur:

                cur.execute("SELECT * FROM customers WHERE UserName=%s;", (str(form.userName.data),))

                row = cur.fetchone()

                if row == None:
                    return "You done Goffed"
                    
#                print(form.userName.data)
#                print(form.passW.data)
#                if row['PassW'] == form.passW.data:
#                    return redirect('/succsess/'+ row['CustomerID'])
#
                else:
                    return redirect('/succsess/'+ row['CustomerID'])



        finally:
            con.close()
        
    return render_template(
    "login.html",
    form=form)


@app.route('/succsess/<data>')
def succsess(data):
    return render_template("succsess.html", message=data)
