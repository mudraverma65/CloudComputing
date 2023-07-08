from flask import Flask, request, jsonify
import pymysql

# RDS database connection details
db_host = 'csci5409-instance-1.cxf4zgkzpmah.us-east-1.rds.amazonaws.com'
db_port = 3306
db_name = 'csci5409'
db_user = 'mudra'
db_password = 'mudra#123'

app = Flask(__name__)

# Create the products table if it doesn't exist
def create_products_table():
    try:
        # Connect to the Aurora MySQL database
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Create the table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS products (
                name varchar(100),
                price varchar(100),
                availability boolean
            );
        """
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)

        conn.commit()
        conn.close()

    except pymysql.Error as e:
        print("Error creating products table:", e)

# Route for /store-products POST request
@app.route('/store-products', methods=['POST'])
def store_products():
    try:
        # Check if the request contains valid JSON
        if not request.is_json:
            return jsonify(message='Invalid request body'), 400
        
        # Extract the products from the JSON
        products = request.json.get('products')

        # Check if products is a list
        if not isinstance(products, list):
            return jsonify(message='Invalid products format'), 400

        # Create the products table if it doesn't exist
        create_products_table()

        # Connect to the Aurora MySQL database
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Empty the products table
        with conn.cursor() as cursor:
            empty_table_query = "DELETE FROM products;"
            cursor.execute(empty_table_query)

        # Insert each product into the database
        with conn.cursor() as cursor:
            for product in products:
                name = product.get('name')
                price = product.get('price')
                availability = product.get('availability')

                # Insert the product into the table
                insert_query = "INSERT INTO products (name, price, availability) VALUES (%s, %s, %s);"
                cursor.execute(insert_query, (name, price, availability))

        conn.commit()
        conn.close()

        return jsonify(message='Success.')

    except pymysql.Error as e:
        return jsonify(message='Error inserting data into the database'), 500

# Route for /list-products GET request
@app.route('/list-products', methods=['GET'])
def list_products():
    try:
        # Create the products table if it doesn't exist
        create_products_table()

        # Connect to the Aurora MySQL database
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Retrieve the products from the database
        with conn.cursor() as cursor:
            select_query = "SELECT name, price, availability FROM products;"
            cursor.execute(select_query)
            products = []
            for row in cursor.fetchall():
                name, price, availability = row
                product = {
                    'name': name,
                    'price': price,
                    'availability': availability
                }
                products.append(product)

        conn.close()

        return jsonify(products=products)

    except pymysql.Error as e:
        return jsonify(message='Error retrieving data from the database'), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
