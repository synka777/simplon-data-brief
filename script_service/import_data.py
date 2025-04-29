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
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    with open(csv_file, "r") as c:
        csvreader = csv.DictReader(c) # Automatically skips header row
        headers = csvreader.fieldnames
        for i, row in enumerate(csvreader):
            try:
                if type == "products":
                    statement = """
                        INSERT INTO products (id, name, price, qty)
                        VALUES (?, ?, ?, ?)
                    """
                    cursor.execute(statement, (
                        row[headers[0]],
                        row[headers[1]],
                        row[headers[2]],
                        row[headers[3]]
                    ))

                elif type == "shops":
                    statement = """
                        INSERT INTO shops (id, city, employees)
                        VALUES (?, ?, ?)
                    """
                    cursor.execute(statement, (
                        row[headers[0]],
                        row[headers[1]],
                        row[headers[2]]
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
                            row[headers[0]],
                            row[headers[1]],
                            row[headers[2]],
                            row[headers[3]]
                        ))
            except Exception as e:
                print(f"[ERROR] A problem happened while inserting line {i + 2}:", row, "\n", e)

    connection.commit()
    connection.close()