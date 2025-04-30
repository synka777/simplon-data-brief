from pathlib import Path
import sqlite3

DB_PATH = None

def create_table(statement):
    error = False
    try:
        print("Creating table... ", end="")
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Activate FK constraints
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute(statement)
        connection.commit()
        print("OK")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        connection.close()
        return False if error else True


def initialize_db_from_sql_file(db_path):
    current_dir = Path(__file__).resolve().parent
    sql_file_path = f"{current_dir}/schema.sql"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    with open(sql_file_path, "r") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    connection.commit()
    connection.close()


def create_db(db_path):
    global DB_PATH
    DB_PATH = db_path
    try:
        initialize_db_from_sql_file(db_path)
        return True
        # # Create the products table
        # products_created = create_table("""
        #     CREATE TABLE IF NOT EXISTS products (
        #         name TEXT,
        #         id VARCHAR PRIMARY KEY,
        #         price DECIMAL(10, 2),
        #         qty INTEGER
        #     );
        # """)

        # # Create the shops table
        # shops_created = create_table("""
        #     CREATE TABLE IF NOT EXISTS shops (
        #         id INTEGER PRIMARY KEY,
        #         city VARCHAR(255),
        #         employees INTEGER
        #     );
        # """)

        # # Create the orders table
        # orders_created = create_table("""
        #     CREATE TABLE IF NOT EXISTS orders (
        #         order_date DATE,
        #         product_id TEXT,
        #         qty INTEGER,
        #         shop_id INTEGER,
        #         FOREIGN KEY (product_id) REFERENCES products(id),
        #         FOREIGN KEY (shop_id) REFERENCES shops(id)
        #     );
        # """)
        # return True if (products_created and shops_created and orders_created) else False
    except Exception as e:
        print('A problem occured during tables creation:', e)
        return False