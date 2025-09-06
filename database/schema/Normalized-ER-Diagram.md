
# Database Design Documentation

This documentation corresponds to **issue #1**.

---

## Information to be Stored

The Little Lemon Restaurant database must store the following:

1. **Bookings**: Information about booked tables, including booking ID, date, and table number.  
2. **Orders**: Details of each order such as order date, quantity, and total cost.  
3. **Order Delivery Status**: Information about delivery date and delivery status.  
4. **Menu**: Details about cuisines, starters, courses, drinks, and desserts.  
5. **Customers**: Customer names and contact details.  
6. **Staff**: Employee roles, salaries, and contact information.  

---

## Main Entities and Attributes

### Customers
- **Primary Key**: Customer_ID  
- **Attributes**: Full_Name, Phone_Number  

### Staff
- **Primary Key**: Staff_ID  
- **Attributes**: Name, Role, Salary, Address, Contact_Number, Email  

### Menu Items
- **Primary Key**: Item_ID  
- **Attributes**: Item_Name, Category, Cuisine, Price  

### Bookings
- **Primary Key**: Booking_ID  
- **Attributes**: Booking_Date, Customer_ID, Table_Number, Number_of_Persons, Staff_ID  

### Orders
- **Primary Key**: Order_ID  
- **Attributes**: Table_Number, Order_Date, Total_Cost, Booking_ID, Items and Quantity  

### Orders Delivery Status
- **Primary Key**: Order_ID  
- **Attributes**: Delivery_Date, Delivery_Status  

---

## Normalization Process

- The **Orders** table originally contained multi-valued attributes (`Items` and `Quantities`).  
- To resolve this, the table was split into two:  

1. **Orders** → Contains general order details (Order_ID, Booking_ID, etc.).  
2. **Orders_Details**  
   - **Primary Key**: (Order_ID, Item_ID)  
   - **Attributes**: Quantity  

This ensures the schema is in **3rd Normal Form (3NF)**.

---

## Final Database Design

The final ERD was designed in **MySQL Workbench**.  

<p align="center">
  <img src="https://user-images.githubusercontent.com/70551007/236650190-ff8b1a48-4d9b-446d-85c7-b7b9cc7a8be6.png" width="600">
</p>

---

## Schema Implementation

The database schema was forward-engineered from MySQL Workbench into MySQL Server.  

### Create Database
```sql
CREATE SCHEMA IF NOT EXISTS `Little_Lemon_DB` DEFAULT CHARACTER SET utf8;
USE `Little_Lemon_DB`;
````

### Example: Bookings Table

```sql
CREATE TABLE IF NOT EXISTS `Little_Lemon_DB`.`Bookings` (
  `Booking_ID` INT NOT NULL,
  `Booking_Date` DATETIME NOT NULL,
  `Customer_ID` INT NOT NULL,
  `Table_number` INT NOT NULL,
  `Number_of_Persons` INT NOT NULL,
  `Staff_ID` INT NOT NULL,
  PRIMARY KEY (`Booking_ID`),
  INDEX `FK_customers_in_bookings_idx` (`Customer_ID` ASC),
  INDEX `FK_staff_in_bookings_idx` (`Staff_ID` ASC),
  CONSTRAINT `FK_customers_in_bookings`
    FOREIGN KEY (`Customer_ID`)
    REFERENCES `Little_Lemon_DB`.`Customers` (`Customer_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_staff_in_bookings`
    FOREIGN KEY (`Staff_ID`)
    REFERENCES `Little_Lemon_DB`.`Staff` (`Staff_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;
```

### Example: Menu Table

```sql
CREATE TABLE IF NOT EXISTS `Little_Lemon_DB`.`Menu` (
  `Item_ID` INT NOT NULL,
  `Name` VARCHAR(45) NOT NULL,
  `Category` VARCHAR(45) NOT NULL,
  `Cuisine` VARCHAR(45) NOT NULL,
  `Price` INT NOT NULL,
  PRIMARY KEY (`Item_ID`)
) ENGINE = InnoDB;
```

---

## Folder Location

This documentation belongs in:

```
/database/schema/Database-Design.md
```

The actual `.sql` files for each table should live under:

```
/database/schema/tables/
```

Example:

```
/database/schema/tables/Bookings.sql
/database/schema/tables/Menu.sql
/database/schema/tables/Customers.sql
...
```
