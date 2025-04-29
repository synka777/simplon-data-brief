import sqlite3

DB_PATH = None

def create_table(statement):
    try:
        print('Creating table... ', end="")
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(statement)
        connection.commit()
        print('OK')
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        connection.close()


def create_db(db_path):
    global DB_PATH
    DB_PATH = db_path
    try:
        create_table("""
            CREATE TABLE IF NOT EXISTS product (
                id VARCHAR PRIMARY KEY,
                name TEXT,
                price DECIMAL,
                qty INTEGER
            );
        """)
        create_table("""
            CREATE TABLE IF NOT EXISTS shop (
                id INTEGER PRIMARY KEY,
                city VARCHAR(255),
                employees INTEGER
            );
        """)
        create_table("""
            CREATE TABLE IF NOT EXISTS orders (
                order_date DATE,
                product_id VARCHAR REFERENCES product(id) ON DELETE CASCADE,
                qty INTEGER,
                shop_id INTEGER REFERENCES shop(id) ON DELETE CASCADE
            );
        """)
        return True
    except Exception as e:
        print('A problem occured during tables creation:', e)
        return False