DROP USER IF EXISTS 'whiskymaster'@'localhost';
DROP DATABASE IF EXISTS whiskymaster;

CREATE DATABASE whiskymaster;

CREATE USER 'whiskymaster'@'localhost' IDENTIFIED BY 'whisky';

GRANT ALL PRIVILEGES ON whiskymaster.* TO 'whiskymaster'@'localhost';

CREATE TABLE whiskymaster.whisky
(
	WhiskyID	int				NOT NULL,
    WhiskyName	VARCHAR(100)	NOT NULL,
    Price		int				NOT NULL,
    StorageLeft int				NOT NULL,
    Nation		VARCHAR(255),
    Distillery	VARCHAR(255),
    Region		VARCHAR(255),
    Alohol		VARCHAR(10)		NOT NULL,
    Sold		int,
    
    Picture 	BOOLEAN			NOT NULL,
	Active		BOOLEAN 		NOT NULL,
    
    PRIMARY KEY(WhiskyID)
    );
    
INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture, Active)
VALUES('1','Nikka Tailord', 1100, 5, 'Japan', 'Nikka', '43.0%', True, True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture, Active)
VALUES('2','Caol Ila The Maltman 6 Years', 900, 10, 'Scotland', 'Caol Ila', '51.6%', True, True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture, Active)
VALUES('3','Penderyn Oloroso Sherry Finish', 800, 5, 'Scotland', 'Penderyn', '59.2%', True, True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture, Active)
VALUES('4','Hibiki Japanese Harmony', 750, 5, 'Japan', 'Suntory Whisky', '43%', True, True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture, Active)
VALUES('5','Bunnahabhain 18', 1300, 3, 'Scotland', 'Bunnahabhain', '46.3%', True, True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture, Active)
VALUES('6','Glenfiddich 21 Reserva Rum Cask Finish', 1400, 2, 'Scotland', 'Glenfiddich', '43.2%', True, True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture, Active)
VALUES('7','Lagavulin 16 Years', 450, 20, 'Scotland', 'Lagavulin', '43%', False, True);

CREATE TABLE whiskymaster.customers
(
	CustomerID	int				NOT Null,
    CorpName	VARCHAR(255)	NOT Null,
    UserName	VARCHAR(255)	NOT Null,
    PassW		VARCHAR(255)	NOT Null,	
    Mail		VARCHAR(255)	NOT Null,
    PNumber		VARCHAR(255)	NOT	Null,
    City		VARCHAR(255)	NOT Null,
    Address		VARCHAR(255)	NOT Null,
    ZipCode		VARCHAR(255)	NOT Null,
    
    unique KEY (UserName),
    unique KEY (Mail),
    PRIMARY KEY(CustomerID)
    
	);
    
INSERT INTO whiskymaster.customers(CustomerID, CorpName, UserName, PassW, Mail, PNumber, City, Address, ZipCode)
VALUES(0, 'Evil', 'cust0', 'root', 'hejo@test.com', '007', 'Cool Town', 'Nowhere street 7', '78563255');
INSERT INTO whiskymaster.customers(CustomerID, CorpName, UserName, PassW, Mail, PNumber, City, Address, ZipCode)
VALUES(1, 'Margo and sons', 'Margo', 'pas', 'margo@margoasons.com', '1231234', 'Margonia', 'mstraze 23','23456');
    
    
CREATE TABLE whiskymaster.reserved
(
	ReservedID		VARCHAR(15)		NOT Null,
    CustomerID		int,
    ReserverDate	VARCHAR(255),
    ReservedStatus	VARCHAR(255),
    Mail			VARCHAR(255),
    PNumber			VARCHAR(255),
    City			VARCHAR(255),
    Adress			VARCHAR(255),
    ZipCode			VARCHAR(255),
    
    PRIMARY KEY(ReservedID),
    FOREIGN KEY (CustomerID) REFERENCES whiskymaster.customers(CustomerID)
    

    
	);
    
    
CREATE TABLE whiskymaster.grading
(
	GradingID		VARCHAR(15)		NOT Null,
    Grade			int				NOT Null,
    ProductNumber	int				NOT NUll,
    UserID			int		NOT NUll,
    
    PRIMARY KEY(GradingID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.whisky(WhiskyID),
    FOREIGN KEY (UserID) REFERENCES whiskymaster.customers(CustomerID)
    
    
	);
    
CREATE TABLE whiskymaster.reservedProduct
(
	ID				VARCHAR(15)		NOT Null,
    ReservedID		VARCHAR(15)		NOT Null,
    Quantity		int				NOT NUll,
    ProductNumber	int				NOT NUll,
    Price			int				NOT NULL,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (ReservedID) REFERENCES whiskymaster.reserved(ReservedID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.whisky(WhiskyID)
    
    
	);

CREATE TABLE whiskymaster.comments
(
	ID				int				NOT Null,
    UserName		VARCHAR(255)	NOT Null,		
    Comments		VARCHAR(511)	NOT Null,
	UserID			int				NOT NUll,
    ProductNumber	int				NOT Null,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (UserID) REFERENCES whiskymaster.customers(CustomerID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.whisky(WhiskyID),
    FOREIGN KEY (UserName) REFERENCES whiskymaster.customers(UserName)
    
	);
    
INSERT INTO whiskymaster.comments(ID, UserName, Comments, UserID, ProductNumber)
VALUES(0, (SELECT UserName FROM whiskymaster.customers Where UserName='Cust0'), "Jag Tycker om den", (SELECT CustomerID FROM whiskymaster.customers Where CustomerID=0), (SELECT WhiskyID FROM whiskymaster.whisky Where WhiskyID=1));


CREATE TABLE whiskymaster.admins
(
	ID				VARCHAR(15)		NOT Null,
    UserName		VARCHAR(511)	NOT Null,
    Passw			VARCHAR(255)	NOT NUll,
    FirstName		VARCHAR(255)	NOT NULL,
    
    PRIMARY KEY(ID),
    UNIQUE KEY(UserName)
    
	);
    
INSERT INTO whiskymaster.admins(ID, UserName, Passw, FirstName)
VALUES('0', 'admin', 'admin', 'adminsson');
    
CREATE TABLE whiskymaster.Basket
(
	ID			int				NOT Null,
    CustomerID	int				NOT NUll,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (CustomerID) REFERENCES whiskymaster.customers(CustomerID)
    
	);
    
CREATE TABLE whiskymaster.BasketProduct
(
	ID				int				NOT Null,
    Quantity		int				NOT Null,
	BasketID		int				NOT NUll,
    ProductNumber	int				NOT NUll,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (BasketID) REFERENCES whiskymaster.Basket(ID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.whisky(WhiskyID)
    
	);


#UPDATE whiskymaster.whisky SET StorageLeft=120 WHERE WhiskyID='1';

#SELECT * FROM basketproduct WHERE BasketID IN (SELECT ID FROM basket WHERE CustomerID=0);

#SELECT SUM(Price) FROM whiskymaster.whisky;
#create temporary table basketTmp(SELECT * FROM whiskymaster.BasketProduct WHERE BasketID IN (SELECT ID FROM Basket WHERE CustomerID=0));
#select * from whisky inner join basketTmp on whisky.WhiskyID=basketTmp.ProductNumber;
#create temporary table basketPrice(SELECT * FROM whisky inner join basketTmp on  whisky.WhiskyID=basketTmp.ProductNumber);
#Drop table basketPrice;

#SELECT SUM(Price * Quantity) FROM basketPrice;

#SELECT ProductNumber, SUM(Quantity) AS Quantity, COUNT(ProductNumber) AS COUNT FROM  whiskymaster.BasketProduct GROUP BY ProductNumber;



#UPDATE whiskymaster.Whisky SET StorageLeft = 15 WHERE WhiskyID = '1';
