CREATE TABLE PRODUCTS (
    ProductID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    Price DECIMAL(10, 2),
    Stock INT
);
 CREATE TABLE SUPPLIERS (
    SupplierID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    ContactName VARCHAR(100),
    PhoneNumber VARCHAR(15)
);

CREATE TABLE Stock(
    StockID INT PRIMARY KEY,
    ProductID INT,
    SupplierID INT,
    Quantity INT,
    FOREIGN KEY (ProductID) REFERENCES PRODUCTS(ProductID),
    FOREIGN KEY (SupplierID) REFERENCES SUPPLIERS(SupplierID)
);

INSERT INTO PRODUCTS (ProductID, Name, Description, Price, Stock) VALUES
(1, 'Laptop', 'High performance laptop', 75000.00, 50),
(2, 'Smartphone', 'Latest model smartphone', 30000.00, 150),
(3, 'Headphones', 'Noise cancelling headphones', 5000.00, 200),
(4, 'Monitor', '24 inch LED monitor', 12000.00, 80);

INSERT INTO SUPPLIERS (SupplierID, Name, ContactName, PhoneNumber) VALUES
(1, 'Tech Supplies Co.', 'John Doe', '555-1111'),
(2, 'Gadget World', 'Jane Smith', '555-2222'),
(3, 'ElectroMart', 'Mike Johnson', '555-3333');

INSERT INTO Stock (StockID, ProductID, SupplierID, Quantity) VALUES
(1, 1, 1, 20),
(2, 2, 2, 50),
(3, 3, 3, 100),
(4, 4, 1, 30);

SELECT ProductID, Name, Stock
FROM PRODUCTS
WHERE Stock < 10;