import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",       # Database host
        user="root",            # Database username
        password="root@123",    # Database password
        database="mydatabase"   # Database name
    )
    print("Successfully connected to the database!")
    connection.close()  # Close the connection after testing
except mysql.connector.Error as err:
    print(f"Error: {err}")
