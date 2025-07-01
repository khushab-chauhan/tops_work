create database Assessment;
use Assessment;
CREATE TABLE Salesman (
    salesman_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100),
    commission DECIMAL(5,2)
);
INSERT INTO Salesman (salesman_id, name, city, commission) VALUES
(101, 'John Doe', 'New York', 0.15),
(102, 'Sarah Smith', 'London', 0.12),
(103, 'Raj Kumar', 'Mumbai', 0.10);
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    grade INT,
    salesman_id INT,
    FOREIGN KEY (salesman_id) REFERENCES Salesman(salesman_id)
);
INSERT INTO Customer (customer_id, customer_name, city, grade, salesman_id) VALUES
(1, 'Alice', 'New York', 100, 101),
(2, 'Bob', 'London', 200, 102),
(3, 'Charlie', 'Delhi', 150, 103),
(4, 'Diana', 'Mumbai', 300, 103);


SELECT 
    c.customer_name AS "Customer Name",
    c.city AS "Customer City",
    s.name AS "Salesman Name",
    s.commission AS "Commission"
FROM 
    Customer c
JOIN 
    Salesman s
ON 
    c.salesman_id = s.salesman_id;