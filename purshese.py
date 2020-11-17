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

            cur.execute("SELECT MAX(ID) FROM Basket;")

            maxID = cur.fetchone()

    finally:

        con.close()

    if maxID == None:
        maxID = 0;

    con = getConnection()
    try:
        with con.cursor() as cur:

            cur.execute("INSERT INTO Basket( ID, CustomerID) VALUES (%d, %s)", ((maxID + 1), userID))
            cur.commit()

    finally:

        con.close()



def addToBasket(whiskyID, count):

    userID = request.cookies.get('userID')
    con = getConnection()
    try:

        with con.cursor() as cur:

            cur.execute("SELECT * FROM Basket WHERE CustomerID=%s;", (userID,))

            basket = cur.fetchone()

    finally:

        con.close()

    if basket == None:
        createBasket(userID)

        con = getConnection()
        try:

            with con.cursor() as cur:

                cur.execute("SELECT ID FROM Basket WHERE CustomerID=%s;", (userID,))

                basketID = cur.fetchone()

        finally:

            con.close()

    con = getConnection()
    try:
        with con.cursor() as cur:

            cur.execute("SELECT MAX(ID) FROM BasketProduct;")

            maxID = cur.fetchone()

    finally:

        con.close()

    if maxID == None:
        maxID = 0;

    con = getConnection()
    try:

        with con.cursor() as cur:

            cur.execute("INSERT INTO BasketProduct( ID, Quantity, BasketID, ProductNumber) VALUES (%d, %d, %s, %s)", ((maxID + 1), count, basketID, whiskyID))
            cur.commit()

    finally:
        con.close()
