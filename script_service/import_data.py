import requests
import sqlite3
import json
import csv


def download_csv(url, dest):
    response = requests.get(url)

    if response.status_code == 200:
        # Will overwrite the old csv files with updated ones next time it runs
        with open(dest, "wb") as file:
            file.write(response.content)
        return True
    else:
        print(f"\nFailed to download the file. Status code: {response.status_code}")
        return False


def load_sources(json_path):
    with open(json_path) as j:
        return json.load(j)


def insert_data(type, csv_file, db_path):
    # Ensure the connection is closed at the end by using "with"
    with sqlite3.connect(db_path) as connection:
        error = False
        cursor = connection.cursor()

        # Enable foreign key constraints for the session
        cursor.execute("PRAGMA foreign_keys = ON;")

        with open(csv_file, "r") as c:
            csvreader = csv.DictReader(c)  # Ignores the first line (header)
            headers = csvreader.fieldnames
            for i, row in enumerate(csvreader):
                try:
                    if type == "products":
                        statement = """
                            INSERT INTO products (name, id, price, qty)
                            VALUES (?, ?, ?, ?)
                        """
                        cursor.execute(statement, (
                            row[headers[0]],  # name
                            row[headers[1]],  # id
                            row[headers[2]],  # price
                            row[headers[3]]   # qty
                        ))

                    elif type == "shops":
                        statement = """
                            INSERT INTO shops (id, city, employees)
                            VALUES (?, ?, ?)
                        """
                        cursor.execute(statement, (
                            row[headers[0]],  # id
                            row[headers[1]],  # city
                            row[headers[2]]   # employees
                        ))

                    elif type == "orders":
                        # Check if the combination of values is not already in DB before inserting
                        cursor.execute("""
                            SELECT 1 FROM orders
                            WHERE order_date = ? AND product_id = ? AND qty = ? AND shop_id = ?
                        """, (row[headers[0]], row[headers[1]], row[headers[2]], row[headers[3]]))

                        if cursor.fetchone() is None:
                            # Then do the insertion
                            statement = """
                                INSERT INTO orders (order_date, product_id, qty, shop_id)
                                VALUES (?, ?, ?, ?)
                            """
                            cursor.execute(statement, (
                                row[headers[0]],  # order_date
                                row[headers[1]],  # product_id
                                row[headers[2]],  # qty
                                row[headers[3]]   # shop_id
                            ))
                except Exception as e:
                    print(f"[ERROR] A problem happened while inserting line {i + 2}:", row, "\n", e)
                    error = True

        connection.commit()

        return False if error else True
