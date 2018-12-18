SELECT * FROM Customers
WHERE Country="Germany" AND City="Berlin";

SELECT * FROM Customers
ORDER BY Country DESC;

SELECT * FROM Customers
ORDER BY Country ASC, CustomerName DESC;

INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
VALUES ("Cardinal", "Tom B. Erichsen", "Skagen 21", "Stavanger", "4006", "Norway");

INSERT INTO Customers (CustomerName, City, Country)
VALUES ("Cardinal", "Stavanger", "Norway");

SELECT CustomerName, ContactName, Address
FROM Customers
WHERE Address IS NULL;

UPDATE Customers
SET ContactName = "Alfred Schmidt", City= "Frankfurt"
WHERE CustomerID = 1;

DELETE FROM Customers WHERE CustomerName="Alfreds Futterkiste";

SELECT * FROM Customers
WHERE ROWNUM <= 3;

SELECT MAX(Price) AS LargestPrice
FROM Products;

SELECT SUM(Quantity)
FROM OrderDetails;