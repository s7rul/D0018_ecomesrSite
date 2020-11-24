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
    
    PRIMARY KEY(WhiskyID)
    );
    
INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture)
VALUES('1','Nikka Tailord', 1100, 5, 'Japan', 'Nikka', '43.0%', True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture)
VALUES('2','Caol Ila The Maltman 6 Years', 900, 10, 'Scotland', 'Caol Ila', '51.6%', True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture)
VALUES('3','Penderyn Oloroso Sherry Finish', 800, 5, 'Scotland', 'Penderyn', '59.2%', True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture)
VALUES('4','Hibiki Japanese Harmony', 750, 5, 'Japan', 'Suntory Whisky', '43%', True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture)
VALUES('5','Bunnahabhain 18', 1300, 3, 'Scotland', 'Bunnahabhain', '46.3%', True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture)
VALUES('6','Glenfiddich 21 Reserva Rum Cask Finish', 1400, 2, 'Scotland', 'Glenfiddich', '43.2%', True);

INSERT INTO whiskymaster.whisky(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Picture)
VALUES('7','Lagavulin 16 Years', 450, 20, 'Scotland', 'Lagavulin', '43%', False);

CREATE TABLE whiskymaster.customers
(
	CustomerID	VARCHAR(15)		NOT Null,
    CorpName	VARCHAR(255),
    UserName	VARCHAR(255)	NOT Null,
    PassW		VARCHAR(255)	NOT Null,	
    Mail		VARCHAR(255),
    PNumber		VARCHAR(255),
    City		VARCHAR(255),
    Address		VARCHAR(255),
    ZipCode		VARCHAR(255),
    
    unique KEY (UserName),
    PRIMARY KEY(CustomerID)
    
	);
    
INSERT INTO whiskymaster.customers(CustomerID, UserName, PassW)
VALUES('0', 'cust0', 'root');
INSERT INTO whiskymaster.customers(CustomerID, CorpName, UserName, PassW, Mail, PNumber, City, Address, ZipCode)
VALUES('1', 'Margo and sons', 'Margo', 'pas', 'margo@margoasons.com', '1231234', 'Margonia', 'mstraze 23','23456');
    
    
CREATE TABLE whiskymaster.reserved
(
	ReservedID		VARCHAR(15)		NOT Null,
    CustomerID		VARCHAR(255),
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
    ProductNumber	VARCHAR(15)		NOT NUll,
    UserID			VARCHAR(15)		NOT NUll,
    
    PRIMARY KEY(GradingID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.whisky(WhiskyID),
    FOREIGN KEY (UserID) REFERENCES whiskymaster.customers(CustomerID)
    
    
	);
    
CREATE TABLE whiskymaster.reservedProduct
(
	ID				VARCHAR(15)		NOT Null,
    ReservedID		VARCHAR(15)		NOT Null,
    Quantity		int				NOT NUll,
    ProductNumber	VARCHAR(15)		NOT NUll,
    Price			int				NOT NULL,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (ReservedID) REFERENCES whiskymaster.reserved(ReservedID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.whisky(WhiskyID)
    
    
	);

CREATE TABLE whiskymaster.comments
(
	ID				VARCHAR(15)		NOT Null,
    comments		VARCHAR(511)	NOT Null,
	UserID			VARCHAR(15)		NOT NUll,
    ProductNumber	VARCHAR(15)		NOT NUll,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (UserID) REFERENCES whiskymaster.customers(CustomerID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.whisky(WhiskyID)
    
	);

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
    CustomerID	VARCHAR(15)		NOT NUll,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (CustomerID) REFERENCES whiskymaster.customers(CustomerID)
    
	);
    
CREATE TABLE whiskymaster.BasketProduct
(
	ID				int				NOT Null,
    Quantity		int				NOT Null,
	BasketID		int				NOT NUll,
    ProductNumber	VARCHAR(15)		NOT NUll,
    
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
