CREATE DATABASE IF NOT EXISTS vehicle_rental_db;
USE vehicle_rental_db;

DROP TABLE IF EXISTS rental;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL
);

CREATE TABLE vehicle (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    registration_no VARCHAR(20) NOT NULL UNIQUE,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    vehicle_year YEAR NOT NULL,
    rental_price_per_day DECIMAL(10,2) NOT NULL,
    status ENUM('Available','Rented','Maintenance') DEFAULT 'Available',
    CONSTRAINT fk_vehicle_category
        FOREIGN KEY (category_id) REFERENCES category(category_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE rental (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    rental_date DATE NOT NULL,
    return_date DATE,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('Booked','Ongoing','Completed','Cancelled','Returned') DEFAULT 'Booked',
    CONSTRAINT fk_rental_customer
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_rental_vehicle
        FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

INSERT INTO category (category_name) VALUES
('Hatchback'), ('Sedan'), ('SUV'), ('Luxury');

INSERT INTO customer (name, email, phone) VALUES
('Sneha Patel', 'sneha@example.com', '9876543210'),
('Amit Kumar', 'amit@example.com', '9876543211'),
('Priya Singh', 'priya@example.com', '9876543212'),
('Rahul Sharma', 'rahul@example.com', '9876543213');

INSERT INTO vehicle
(category_id, registration_no, brand, model, vehicle_year, rental_price_per_day, status)
VALUES
(1, 'MH12AB1234', 'Hyundai', 'Creta', 2022, 1600.00, 'Available'),
(2, 'MH12CD5678', 'Hyundai', 'i20', 2021, 1200.00, 'Available'),
(2, 'MH12EF9012', 'Royal Enfield', 'Classic 350', 2022, 900.00, 'Available'),
(3, 'MH12GH3456', 'Toyota', 'Innova', 2023, 2600.00, 'Available'),
(3, 'MH12IJ7890', 'Toyota', 'Innova', 2024, 2800.00, 'Available');

-- Useful DBMS queries
SELECT * FROM category;
SELECT * FROM customer;
SELECT * FROM vehicle;
SELECT * FROM rental;

-- JOIN query used by the Flask booking page
SELECT
    r.rental_id,
    c.name,
    v.brand,
    v.model,
    r.rental_date,
    r.return_date,
    r.total_amount,
    r.status
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
JOIN vehicle v ON r.vehicle_id = v.vehicle_id
ORDER BY r.rental_id DESC;

-- Check rental status definition
SHOW COLUMNS FROM rental LIKE 'status';

-- Return functionality used by the application:
-- UPDATE rental SET status = 'Returned', return_date = CURDATE() WHERE rental_id = ?;
-- UPDATE vehicle SET status = 'Available' WHERE vehicle_id = ?;
