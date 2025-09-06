
---

# Database Client Setup

This documentation corresponds to **issue #6**.

---

## Overview
Little Lemon Restaurant requires a **Python-based database client** to interact with the MySQL database.  
The client is implemented using the `mysql-connector-python` library.

The workflow includes:
1. Establishing a connection to the database.  
2. Creating a cursor object.  
3. Executing queries to retrieve and manipulate data.

---

## 1. Install Required Dependencies
Install the MySQL connector library:

```bash
pip install mysql-connector-python
````

---

## 2. Connecting Python to the Database

First, import the connector and establish the connection using environment variables for credentials.

```python
import mysql.connector as connector
import os

connection = connector.connect(
    user=os.getenv("ENV_DATABASE_USER"),
    password=os.getenv("ENV_DATABASE_PASSWORD"),
    host=os.getenv("ENV_DATABASE_HOST"),
    port=os.getenv("ENV_DATABASE_PORT")
)
```

> ⚠️ **Best practice**: Never hardcode credentials. Store them securely in environment variables or a `.env` file.

---

## 3. Initializing the Cursor and Selecting the Database

```python
cursor = connection.cursor()

use_database = """USE Little_Lemon_DB;"""
cursor.execute(use_database)
```

This links the Python application to the **Little\_Lemon\_DB** schema.

---

## 4. Example Tasks Performed

### (a) Show All Tables in the Database

```python
show_tables_query = """SHOW TABLES;""" 
cursor.execute(show_tables_query)
results = cursor.fetchall()

for i, result in enumerate(results, start=1):
    print(f"Table no. {i}: {result[0]}")
```

**Output:**

```
Table no. 1 : bookings
Table no. 2 : customers
Table no. 3 : menu
Table no. 4 : orders
Table no. 5 : orders_delivery_status
Table no. 6 : orders_details
Table no. 7 : ordersview
Table no. 8 : staff
```

---

### (b) Identify Customers Who Spent More Than \$60

This query is useful for targeting customers for a **promotional campaign**.

```python
promotional_campaign = """
    SELECT C.Full_Name, C.Phone_Number, O.Total_Cost
    FROM Customers AS C
    INNER JOIN Bookings AS B
        ON B.Customer_ID = C.Customer_ID
    INNER JOIN Orders AS O
        ON O.Booking_ID = B.Booking_ID
    WHERE O.Total_Cost > 60;
"""

cursor.execute(promotional_campaign)
results = cursor.fetchall()

print("Information about customers for the promotional campaign:")

for i, result in enumerate(results, start=1):
    print(f"Customer no. {i}: {result[0]} (Contact: {result[1]}) paid ${result[2]}.")
```

**Output:**

```
Information about customers for the promotional campaign:
Customer no. 1: Rabia Mendoza (Contact: 0123456789) paid $890.
Customer no. 2: Aayan Chaney (Contact: 0129876543) paid $800.
```

---

## 5. Closing the Connection

Always close the cursor and connection when finished:

```python
cursor.close()
connection.close()
```

---

## Conclusion

With this Python client:

* Little Lemon can **query, monitor, and analyze** data programmatically.
* Business teams can leverage insights (like customer spending habits) for targeted **marketing and operations**.

This document belongs in the following project folder:

```
/clients/Database-Client-Setup.md
```

