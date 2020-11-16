DROP USER IF EXISTS 'whiskymaster'@'localhost';
DROP DATABASE IF EXISTS whiskymaster;

CREATE DATABASE whiskymaster;

CREATE USER 'whiskymaster'@'localhost' IDENTIFIED BY 'whisky';

GRANT ALL PRIVILEGES ON whiskymaster.* TO 'whiskymaster'@'localhost';

CREATE TABLE whiskymaster.WHISKY
(
	WhiskyID	VARCHAR(15)		NOT NULL,
    WhiskyName	VARCHAR(100)	NOT NULL,
    Price		VARCHAR(255)	NOT NULL,
    StorageLeft int				NOT NULL,
    Nation		VARCHAR(255),
    Distillery	VARCHAR(255),
    Region		VARCHAR(255),
    Alohol		VARCHAR(10)		NOT NULL,
    Sold		int,
    
    #Placeholder
    Picture 	VARCHAR(255),
    
    PRIMARY KEY(WhiskyID)
    );
    
INSERT INTO whiskymaster.WHISKY(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol, Region)
VALUES('1','Nikka Tailord', '1100', 5, 'Japan', 'Nikka', '43.0%', 'Test');

INSERT INTO whiskymaster.WHISKY(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol)
VALUES('2','Caol Ila The Maltman 6 Years', '900', 10, 'Scotland', 'Caol Ila', '51.6%');

INSERT INTO whiskymaster.WHISKY(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol)
VALUES('3','Penderyn Oloroso Sherry Finish', '800', 5, 'Scotland', 'Penderyn', '59.2%');

INSERT INTO whiskymaster.WHISKY(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol)
VALUES('4','Hibiki Japanese Harmony', '750', 5, 'Japan', 'Suntory Whisky', '43%');

INSERT INTO whiskymaster.WHISKY(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol)
VALUES('5','Bunnahabhain 18', '1300', 3, 'Scotland', 'Bunnahabhain', '46.3%');

INSERT INTO whiskymaster.WHISKY(WhiskyID, WhiskyName, Price, StorageLeft,
Nation, Distillery, Alohol)
VALUES('6','Glenfiddich 21 Reserva Rum Cask Finish', '1400', 2, 'Scotland', 'Glenfiddich', '43.2%');

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
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.WHISKY(WhiskyID),
    FOREIGN KEY (UserID) REFERENCES whiskymaster.customers(CustomerID)
    
    
	);
    
CREATE TABLE whiskymaster.reservedProduct
(
	ID				VARCHAR(15)		NOT Null,
    ReservedID		VARCHAR(15)		NOT Null,
    Quantity		int				NOT NUll,
    ProductNumber	VARCHAR(15)		NOT NUll,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (ReservedID) REFERENCES whiskymaster.reserved(ReservedID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.WHISKY(WhiskyID)
    
    
	);

CREATE TABLE whiskymaster.comments
(
	ID				VARCHAR(15)		NOT Null,
    comments		VARCHAR(511)	NOT Null,
	UserID			VARCHAR(15)		NOT NUll,
    ProductNumber	VARCHAR(15)		NOT NUll,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (UserID) REFERENCES whiskymaster.customers(CustomerID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.WHISKY(WhiskyID)
    
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
    
CREATE TABLE whiskymaster.Basket
(
	ID			VARCHAR(15)		NOT Null,
    CustomerID	VARCHAR(15)		NOT NUll,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (CustomerID) REFERENCES whiskymaster.customers(CustomerID)
    
	);
    
CREATE TABLE whiskymaster.BasketProduct
(
	ID				VARCHAR(15)		NOT Null,
    Quantity		int				NOT Null,
	BasketID		VARCHAR(15)		NOT NUll,
    ProductNumber	VARCHAR(15)		NOT NUll,
    
    PRIMARY KEY(ID),
    FOREIGN KEY (BasketID) REFERENCES whiskymaster.Basket(ID),
    FOREIGN KEY (ProductNumber) REFERENCES whiskymaster.WHISKY(WhiskyID)
    
	);


#UPDATE whiskymaster.Whisky SET StorageLeft=120 WHERE WhiskyID='1';
