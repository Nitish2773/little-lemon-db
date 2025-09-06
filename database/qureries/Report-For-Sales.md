
# Reports and Stored Procedure Documentation

This documentation corresponds to **issue #3**.

---

## Overview
Little Lemon Restaurant requires several SQL reports and database features to monitor operations and manage bookings.  

Key requirements include:
- **Reports**:  
  - Orders placed in the restaurant  
  - Customers with high-value orders  
  - Menu items ordered frequently  
- **Database operations**:  
  - Delete orders  
  - Check bookings  
  - Add valid bookings  
  - Update bookings  
  - Cancel bookings  

To achieve these, SQL features such as **Views**, **Stored Procedures**, **Triggers**, and **Prepared Statements** are utilized.

---

## Reports

### Task 1: Orders Placed in the Restaurant
A view called `OrdersView` shows order details such as `OrderID`, `Quantity`, and `Total_Cost`.

```sql
SELECT * FROM OrdersView;
````

**Result:**

```
+---------+----------+------------+
| OrderID | Quantity | Total_Cost |
+---------+----------+------------+
|       1 |        7 |        890 |
|       2 |        6 |        800 |
+---------+----------+------------+
```

---

### Task 2: Customers with Orders Costing More than \$150

```sql
SELECT C.Customer_ID, C.Full_Name, O.Order_ID, (M.Item_ID * M.Price) AS Cost, M.Name AS MenuName
FROM Customers AS C
INNER JOIN Bookings AS B
    ON B.Customer_ID = C.Customer_ID
INNER JOIN Orders AS O
    ON O.Booking_ID = B.Booking_ID
INNER JOIN Orders_Details AS OD
    ON OD.OrderID = O.Order_ID
INNER JOIN Menu AS M
    ON M.Item_ID = OD.Item_ID
WHERE O.Total_Cost > 150;
```

**Result:**

```
+-------------+---------------+----------+------+----------+
| Customer_ID | Full_Name     | Order_ID | Cost | MenuName |
+-------------+---------------+----------+------+----------+
|           1 | Rabia Mendoza |        1 |  150 | Pasta    |
|           1 | Rabia Mendoza |        1 |  140 | Salad    |
|           2 | Aayan Chaney  |        2 |  150 | Pasta    |
|           2 | Aayan Chaney  |        2 |  300 | Fried    |
+-------------+---------------+----------+------+----------+
```

---

### Task 3: Menu Items with More Than 2 Orders

```sql
SELECT Name AS MenuName
FROM Menu
WHERE Name = ANY(
    SELECT M.Name
    FROM Menu AS M
    INNER JOIN Orders_Details AS OD
        ON OD.Item_ID = M.Item_ID
);
```

**Result:**

```
+----------+
| MenuName |
+----------+
| Pasta    |
| Salad    |
| Fried    |
+----------+
```

---

## Query Optimization

Performance is critical as data grows. **Stored Procedures** and **Prepared Statements** are used to reduce turnaround time, improve consistency, and simplify query execution.

---

## Stored Procedures & Features

### Task 1: Maximum Ordered Quantity

Procedure: `GetMaxQuantity()`

```sql
CALL GetMaxQuantity();
```

**Result:**

```
+-----------------------+
| Max Quantity in Order |
+-----------------------+
|                     7 |
+-----------------------+
```

---

### Task 2: Return Information About an Order

Prepared Statement: `GetOrderDetail`

```sql
SET @id = 1;
EXECUTE GetOrderDetail USING @id;
```

**Result:**

```
+---------+----------+------------+
| OrderID | Quantity | Total_Cost |
+---------+----------+------------+
|       1 |        7 |        890 |
+---------+----------+------------+
```

---

### Task 3: Delete a Specific Order

Procedure: `CancelOrder(order_id)`

```sql
CALL CancelOrder(1);
```

**Result:**

```
+---------------------+
| Confirmation        |
+---------------------+
| Order 1 is canceled |
+---------------------+
```

---

### Task 4: Check Booking Status

Procedure: `CheckBooking(booking_date, table_number)`

```sql
CALL CheckBooking("2022-08-10 12:00:00", 5);
```

**Result:**

```
+----------------------------+
| Booking Status             |
+----------------------------+
| Table 5 is already booked. |
+----------------------------+
```

---

### Task 5: Add Valid Booking

Procedure: `AddValidBooking(booking_date, table_number, customer_id, num_persons)`

* If table is already booked:

```sql
CALL AddValidBooking("2022-08-10 12:00:00", 5, 1, 5);
```

**Result:**

```
| Table 5 is already booked. Booking cancelled. |
```

* If booking date is available:

```sql
CALL AddValidBooking("2022-10-10 12:00:00", 5, 1, 5);
```

**Result:**

```
| Table 5 is booked for you. |
```

---

### Task 6: Update Booking

Procedure: `UpdateBooking(booking_id, new_date)`

```sql
CALL UpdateBooking(2, "2022-09-20 03:30");
```

**Result:**

```
| Booking 2 is updated. |
```

---

### Task 7: Cancel Booking

Procedure: `CancelBooking(booking_id)`

```sql
CALL CancelBooking(2);
```

**Result:**

```
| Booking 2 is cancelled. |
```

---

## Folder Location

This documentation belongs in:

```
/database/queries/Report-For-Sales.md
```


