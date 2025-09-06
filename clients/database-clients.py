# ----------------------------------------
# Little Lemon Database Client (Simplified)
# ----------------------------------------

import mysql.connector as connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ----------------------------------------
# 1. Establish the connection
# ----------------------------------------
ENV_DATABASE_USER = os.getenv("DATABASE_USER")
ENV_DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
ENV_DATABASE_HOST = os.getenv("DATABASE_HOST")
ENV_DATABASE_PORT = os.getenv("DATABASE_PORT")

connection = connector.connect(
    user=ENV_DATABASE_USER,
    password=ENV_DATABASE_PASSWORD,
    host=ENV_DATABASE_HOST,
    port=ENV_DATABASE_PORT
)

cursor = connection.cursor()
cursor.execute("USE Little_Lemon_DB;")

# ----------------------------------------
# 2. Show tables in the database
# ----------------------------------------
show_tables_query = "SHOW TABLES;"
cursor.execute(show_tables_query)
results = cursor.fetchall()

print("Available tables in the database:")
for i, result in enumerate(results, start=1):
    print(f"Table no. {i}: {result[0]}")

# ----------------------------------------
# 3. Promotional campaign query
# ----------------------------------------
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

print("\nInformation about customers for the promotional campaign:")
for i, (full_name, phone, total_cost) in enumerate(results, start=1):
    print(f"Customer no. {i}: {full_name} (Contact: {phone}) paid ${total_cost}.")

# ----------------------------------------
# 4. Close the connection
# ----------------------------------------
cursor.close()
connection.close()
print("\nDatabase connection closed successfully.")
