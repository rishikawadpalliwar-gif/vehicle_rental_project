
🚀 Live App

""Open App" (https://img.shields.io/badge/🚀%20OPEN%20APP-Vehicle%20Rental%20Management%20System-brightgreen?style=for-the-badge)" (https://rishikawadpalliwar-gif.github.io/vehicle_rental_project/)

Vehicle Rental Management System
# Vehicle Rental Management System

A simple DBMS mini project built with **Python Flask, MySQL, HTML and CSS**.

## Features

- Vehicle listing
- Customer listing
- Vehicle booking/rental
- Rental/booking records
- Return vehicle
- Automatic vehicle availability update
- MySQL relational database
- JOIN queries
- ENUM status constraints
- CRUD-oriented database operations

## Project Structure

```text
vehicle_rental_project/
├── app.py
├── database.py
├── requirements.txt
├── vehicle_rental_database.sql
├── README.md
├── report/
│   └── Vehicle_Rental_Project_Report.pdf
├── screenshots/
├── static/
│   └── style.css
└── templates/
    ├── index.html
    ├── vehicles.html
    ├── customer.html
    ├── rental.html
    └── booking.html
```

## Setup

1. Install Python.
2. Install MySQL Server and MySQL Workbench.
3. Create the database using `vehicle_rental_database.sql`.
4. Open `database.py`.
5. Replace `YOUR_MYSQL_PASSWORD` with your MySQL root password.
6. Open a terminal in this folder.
7. Run:

```bash
pip install -r requirements.txt
python app.py
```

8. Open:

```text
http://127.0.0.1:5000/
```

## Database

Database name:

```text
vehicle_rental_db
```

The SQL script contains the tables:

- category
- vehicle
- customer
- rental

The rental status values include:

```text
Booked
Ongoing
Completed
Cancelled
Returned
```

## Important

Do not upload your real MySQL password to GitHub. Replace it with an environment variable before publishing a public repository.
