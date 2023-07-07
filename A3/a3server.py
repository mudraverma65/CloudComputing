import pymysql

# RDS database connection details
db_host = 'csci5409-instance-1.cxf4zgkzpmah.us-east-1.rds.amazonaws.com'
db_port = 3306
db_user = 'mudra'
db_password = 'mudra#123'

# Connect to the Aurora MySQL database
try:
    conn = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password
    )
    print("Connected to the Aurora MySQL database!")

    # Create a new database
    create_db_query = "CREATE DATABASE csci5409;"
    with conn.cursor() as cursor:
        cursor.execute(create_db_query)
    conn.commit()
    print("Database created successfully!")

    # Switch to the newly created database
    conn.select_db('csci5409')

    # SQL statement to create a table
    create_table_query = """
        CREATE TABLE products (
            name varchar(100),
            price varchar(100),
            availability boolean
        );
    """

    # Execute the SQL statement to create the table
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()
    print("Table created successfully!")

except pymysql.Error as e:
    print("Error connecting to the Aurora MySQL database:", e)
    conn = None

finally:
    if conn:
        conn.close()
        print("Connection to the Aurora MySQL database closed.")
