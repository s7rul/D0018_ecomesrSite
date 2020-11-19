### purshuses
from datetime import datetime
from flask import render_template, request, redirect, make_response
from HelloFlask import app
import pymysql
import pymysql.cursors
from HelloFlask.forms.LoginForm import LoginForm
from HelloFlask.sqlConnection import getConnection

def createBasket(userID):
    con = getConnection()

    try:
        with con.cursor() as cur:
            cur.execute("SELECT ID FROM Basket WHERE CustomerID = %s;", (userID,))
            check = cur.fetchone()
            if check != None:
                return
            cur.execute("SET @id = IF(EXISTS(SELECT ID FROM Basket), ((SELECT MAX(ID) FROM Basket) + 1), 0);")
            cur.execute("INSERT INTO Basket( ID, CustomerID) VALUES (@id, %s);", (userID,))
        con.commit()

    finally:

        con.close()



def addToBasket(whiskyID, count):

    userID = request.cookies.get('userID')

    if userID == None:
        return False

    createBasket(userID)

    con = getConnection()
    try:
        with con.cursor() as cur:

            cur.execute("SET @basketid = (SELECT ID from Basket WHERE CustomerID = %s);", (userID,))
            cur.execute("SELECT ProductNumber FROM BasketProduct WHERE ProductNumber = %s AND BasketID = @basketid;", (whiskyID,))
            if cur.fetchone() == None:
                cur.execute("SET @id = IF(EXISTS(SELECT ID FROM Basket), ((SELECT MAX(ID) FROM BasketProduct) + 1), 0);")
                cur.execute("INSERT INTO BasketProduct( ID, Quantity, BasketID, ProductNumber) VALUES (@id, %s, @basketid, %s)", (count, whiskyID))
            else:
                cur.execute("UPDATE BasketProduct SET Quantity=(Quantity + %s) WHERE ProductNumber = %s AND BasketID = @basketid;", (count, whiskyID))
        con.commit()

    finally:
        con.close()

    return True
