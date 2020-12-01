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

def purchaseBasket(userID, basketID):
    con = getConnection()

    try:
        with con.cursor() as cur:
            cur.execute("SET @reservedId = IF(EXISTS(SELECT ReservedID FROM reserved), ((SELECT MAX(ReservedID) FROM reserved) + 1), 0);")
            cur.execute("SET @userId = %s;", (userID,))
            cur.execute("""INSERT INTO
                    reserved( ReservedID, CustomerID, ReserverDate, ReservedStatus, Mail, PNumber, City, Adress, ZipCode)
                    VALUES (@reservedId, %s, %s, %s,
                    (SELECT Mail FROM customers WHERE CustomerID = @userId),
                    (SELECT PNumber FROM customers WHERE CustomerID = @userId),
                    (SELECT City FROM customers WHERE CustomerID = @userId),
                    (SELECT Address FROM customers WHERE CustomerID = @userId),
                    (SELECT ZipCode FROM customers WHERE CustomerID = @userId));""",
                    (userID,"200101", "ordered"))
            cur.execute("SELECT Price, StorageLeft, Quantity, ProductNumber FROM (whisky INNER JOIN BasketProduct ON WhiskyID = ProductNumber) WHERE BasketID = %s;", (basketID,))
            products = cur.fetchall()
            for row in products:
                cur.execute("SET @rpId = IF(EXISTS(SELECT ID FROM reservedProduct), ((SELECT MAX(ID) FROM reservedProduct) + 1), 0);")

                if int(row['StorageLeft']) < int(row['Quantity']):
                    con.rollback()
                    return False

                cur.execute("INSERT INTO reservedProduct(ID, ReservedID, Quantity, ProductNumber, Price)VALUES (@rpID, @reservedId, %s, %s, %s);",
                        (row['Quantity'],
                        row['ProductNumber'],
                        row['Price']))
                cur.execute("DELETE FROM BasketProduct WHERE BasketID = %s;", (basketID,))

        con.commit()

    finally:
        con.close()

    return True


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
                cur.execute("SET @id = IF(EXISTS(SELECT ID FROM BasketProduct), ((SELECT MAX(ID) FROM BasketProduct) + 1), 0);")
                cur.execute("INSERT INTO BasketProduct( ID, Quantity, BasketID, ProductNumber) VALUES (@id, %s, @basketid, %s);", (count, whiskyID))
            else:
                cur.execute("UPDATE BasketProduct SET Quantity=(Quantity + %s) WHERE ProductNumber = %s AND BasketID = @basketid;", (count, whiskyID))
        con.commit()

    finally:
        con.close()

    return True
