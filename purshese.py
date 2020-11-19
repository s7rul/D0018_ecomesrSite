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
            cur.execute(" SET @id = IF(EXISTS(SELECT ID FROM Basket), ((SELECT MAX(ID) FROM Basket) + 1), 0);")
            cur.execute("INSERT INTO Basket( ID, CustomerID) VALUES (@id, %s);", (userID,))
        con.commit()

    finally:

        con.close()



def addToBasket(whiskyID, count):

    userID = request.cookies.get('userID')

    if userID == None:
        return False

    con = getConnection()
    try:

        with con.cursor() as cur:

            cur.execute("SELECT ID FROM Basket WHERE CustomerID=%s;", (userID,))

            basketID = cur.fetchone()

    finally:

        con.close()

    if basketID == None:
        createBasket(userID)

        con = getConnection()
        try:

            with con.cursor() as cur:

                cur.execute("SELECT ID FROM Basket WHERE CustomerID=%s;", (userID,))

                basketID = cur.fetchone()

        finally:

            con.close()

    basketID = basketID['ID']
    con = getConnection()
    try:
        with con.cursor() as cur:

            cur.execute("SELECT MAX(ID) FROM BasketProduct;")

            maxID = cur.fetchone()
            maxID = maxID['MAX(ID)']

    finally:

        con.close()

    if maxID == None:
        maxID = 0;

    con = getConnection()
    try:

        with con.cursor() as cur:
            maxID = maxID + 1

            cur.execute("INSERT INTO BasketProduct( ID, Quantity, BasketID, ProductNumber) VALUES (%s, %s, %s, %s)", (maxID, count, basketID, whiskyID))
        con.commit()

    finally:
        con.close()

    return True
