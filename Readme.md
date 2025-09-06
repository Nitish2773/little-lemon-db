
# 🍋 Little Lemon Restaurant Database  

This repository contains the **Database Engineer Capstone Project (Meta)** for **Little Lemon Restaurant**.  
The goal is to design, implement, and optimize a relational database system, generate meaningful reports, and build client applications to interact with the database.  

---

# 📑 Table of Contents  

1. [Overview](#overview)  
2. [Database Setup](#1-database-setup)  
   * [Data Requirements](#data-requirements)  
   * [Entities & Attributes](#entities--attributes)  
   * [Normalization](#normalization)  
   * [Database Design](#database-design)  
   * [Implementation in MySQL](#implementation-in-mysql)  
3. [Reports](#2-reports)  
   * [Task 1: Orders placed in the restaurant](#task-1-orders-placed-in-the-restaurant)  
   * [Task 2: Customers with orders > $150](#task-2-customers-with-orders--150)  
   * [Task 3: Menu items with more than 2 orders](#task-3-menu-items-with-more-than-2-orders)  
   * [Stored Procedures](#stored-procedures)  
4. [Database Clients](#3-database-clients)  
   * [Python Connection](#python-connection)  
   * [Show All Tables](#show-all-tables)  
   * [Promotional Campaign Customers](#promotional-campaign-customers)  
5. [Project Structure](#4-project-structure)  
6. [How to Run](#how-to-run)  

---

# Overview  

The **Little Lemon Database** stores essential restaurant operations data such as:  

- Customer bookings  
- Orders and order details  
- Menu items  
- Staff information  
- Order delivery statuses  

With this system, Little Lemon Restaurant can:  
✅ Track bookings and reservations  
✅ Manage orders efficiently  
✅ Monitor staff and salaries  
✅ Generate reports for analysis  
✅ Run promotional campaigns using data insights  

---

# 1. Database Setup  

## Data Requirements  

We need to store:  

1. **Bookings** → reservations (id, date, table number).  
2. **Orders** → order details (date, quantity, cost).  
3. **Order delivery status** → delivery date, status.  
4. **Menu** → cuisines, starters, drinks, desserts.  
5. **Customers** → names, contact details.  
6. **Staff** → role, salary, contact details.  

---

## Entities & Attributes  

- **Customers** → `Customer_ID`, Full Name, Phone Number  
- **Staff** → `Staff_ID`, Name, Role, Salary, Address, Contact, Email  
- **Menu Items** → `Item_ID`, Name, Category, Cuisine, Price  
- **Bookings** → `Booking_ID`, Date, Customer, Table No., Persons, Staff  
- **Orders** → `Order_ID`, Table No., Date, Total Cost, Booking_ID  
- **Order Delivery Status** → `Order_ID`, Delivery Date, Status  

---

## Normalization  

- Orders had multi-valued attributes (items, quantities).  
- Solution → split into **Orders** + **Orders_Details**.  

---

## Database Design  

The final schema was designed with **MySQL Workbench**.  

📂 [Normalized ER Diagram](docs/Normalized-ER-Diagram.md)  

![ERD](images/Little-Lemon-Database-ERD.png)  

---

## Implementation in MySQL  

📂 [Database SQL Scripts](sql/LittleLemonDB.sql)  

Example schema creation:  

```sql
CREATE SCHEMA IF NOT EXISTS `little_lemon_db` DEFAULT CHARACTER SET utf8;
USE `little_lemon_db`;
````

Example table (Bookings):

```sql
CREATE TABLE Bookings (
  Booking_ID INT PRIMARY KEY,
  Booking_Date DATETIME NOT NULL,
  Customer_ID INT NOT NULL,
  Table_number INT NOT NULL,
  Number_of_Persons INT NOT NULL,
  Staff_ID INT NOT NULL,
  FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
  FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
) ENGINE=InnoDB;
```

---

# 2. Reports

All report SQL files live in:
📂 [`/sql/reports/`](sql/reports/)

---

## Task 1: Orders placed in the restaurant

```sql
SELECT * FROM OrdersView;
```

Output:

```
+---------+----------+------------+
| OrderID | Quantity | Total_Cost |
+---------+----------+------------+
|       1 |        7 |        890 |
|       2 |        6 |        800 |
+---------+----------+------------+
```

---

## Task 2: Customers with orders > \$150

```sql
SELECT C.Customer_ID, C.Full_Name, O.Order_ID, M.Price, M.Name
FROM Customers AS C
INNER JOIN Bookings AS B ON B.Customer_ID = C.Customer_ID
INNER JOIN Orders AS O ON O.Booking_ID = B.Booking_ID
INNER JOIN Orders_Details AS OD ON OD.OrderID = O.Order_ID
INNER JOIN Menu AS M ON M.Item_ID = OD.Item_ID
WHERE O.Total_Cost > 150;
```

---

## Task 3: Menu items with more than 2 orders

```sql
SELECT M.Name
FROM Menu AS M
INNER JOIN Orders_Details AS OD ON OD.Item_ID = M.Item_ID
GROUP BY M.Name
HAVING COUNT(OD.OrderID) > 2;
```

---

## Stored Procedures

Implemented in 📂 [`/sql/reports/`](sql/reports/)

* `GetMaxQuantity.sql` → Displays max ordered quantity.
* `CancelOrder.sql` → Cancels an order by ID.
* `CheckBooking.sql` → Checks table booking status.
* `AddValidBooking.sql` → Verifies and adds bookings.
* `UpdateBooking.sql` → Updates booking date.
* `CancelBooking.sql` → Cancels a booking and related orders.

---

# 3. Database Clients

Python clients live in:
📂 [`/python-client/`](python-client/)

---

## Python Connection

```python
import mysql.connector as connector
import os
from dotenv import load_dotenv

load_dotenv()

connection = connector.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT")
)
cursor = connection.cursor()
cursor.execute("USE little_lemon_db;")
```

---

## Show All Tables

```python
cursor.execute("SHOW TABLES;")
for i, table in enumerate(cursor.fetchall()):
    print(f"Table {i+1}: {table[0]}")
```

---

## Promotional Campaign Customers

```python
promo_query = """
SELECT C.Full_Name, C.Phone_Number, O.Total_Cost
FROM Customers AS C
INNER JOIN Bookings AS B ON B.Customer_ID = C.Customer_ID
INNER JOIN Orders AS O ON O.Booking_ID = B.Booking_ID
WHERE O.Total_Cost > 60;
"""
cursor.execute(promo_query)
for i, row in enumerate(cursor.fetchall()):
    print(f"Customer {i+1}: {row[0]} (📞 {row[1]}) paid ${row[2]}")
```

Example output:

```
Customer 1: Rabia Mendoza (📞 0123456789) paid $890
Customer 2: Aayan Chaney (📞 0129876543) paid $800
```

---

# 4. Project Structure

```
Little-Lemon-DB/
│── docs/                     # Documentation
│   ├── Database-Client-Setup.md
│   ├── Normalized-ER-Diagram.md
│   └── Report-For-Sales.md
│
│── images/                   # ERD + Tableau diagrams
│   ├── Little-Lemon-Database-ERD.png
│   └── *.png
│
│── python-client/            # Python DB clients
│   ├── database-clients.py
│   └── database-clients.ipynb
│
│── reports/                  # Tableau + Excel
│   ├── LittlelemonSalesReport.twb
│   └── Little-Lemon-Excel-Data.xlsx
│
│── sql/                      # SQL scripts
│   ├── LittleLemonDB.sql
│   ├── testing-queries.sql
│   ├── little-lemon-reports.sql
│   ├── reports/
│   │   ├── AddBooking.sql
│   │   ├── CancelOrder.sql
│   │   ├── GetMaxQuantity.sql
│   │   ├── ...
│
│── .env.example              # Example env file
│── .gitignore
│── README.md
```

---

# 5. How to Run

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Little-Lemon-DB.git
cd Little-Lemon-DB
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```ini
DATABASE_USER=root
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
```

### 3. Install dependencies

```bash
pip install mysql-connector-python python-dotenv
```

### 4. Import database

Run the schema and procedures:

```bash
mysql -u root -p < sql/LittleLemonDB.sql
mysql -u root -p < sql/little-lemon-reports.sql
```

### 5. Run Python client

```bash
python python-client/database-clients.py
```

---


