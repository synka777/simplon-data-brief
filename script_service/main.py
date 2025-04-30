from import_data import load_sources, download_csv, insert_data
from pathlib import Path
import argparse
import sqlite3
import init_db
import os


def get_sales_by_region(db_path):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        query = """
            SELECT
                s.city AS region,
                SUM(o.qty) AS total_sold,
                ROUND(SUM(o.qty * p.price), 2) AS total_revenue
            FROM orders o
            JOIN shops s ON o.shop_id = s.id
            JOIN products p ON o.product_id = p.id
            GROUP BY s.city
            ORDER BY total_revenue DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        print("Sales by region:")
        for row in results:
            print(f"Region: {row[0]} | Units sold: {row[1]} | Revenue: €{row[2]}")


def get_sales_by_product(db_path):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        query = """
            SELECT
                p.name AS product_name,
                SUM(o.qty) AS total_sold,
                ROUND(SUM(o.qty * p.price), 2) AS total_revenue
            FROM orders o
            JOIN products p ON o.product_id = p.id
            GROUP BY p.id
            ORDER BY total_revenue DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        print("Sales by product:")
        for row in results:
            print(f"Product: {row[0]} | Units sold: {row[1]} | Revenue: €{row[2]}")


def get_total_revenue(db_path):
    with sqlite3.connect(db_path) as connection:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT SUM(p.price * o.qty) AS total_revenue
            FROM orders o
            JOIN products p ON o.product_id = p.id
        """)

        # Get the result
        total_revenue = cursor.fetchone()

        if total_revenue:
            print(f"Total revenue: {total_revenue[0]:.2f}")
        else:
            print("No data found")


def parse_args():
    parser = argparse.ArgumentParser(description="Script with optional --dev flag")
    parser.add_argument('--dev', action='store_true', help='Run in dev mode')
    return parser.parse_args()


def main():
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    db_path = "/data/databrief.db" # Default: production (shared volume path)

    args = parse_args()
    if args.dev:
        print("Running in development mode")
        db_path = f"{parent_dir}/shared_data/databrief.db" # DB location for dev mode

    if not Path.exists(Path(db_path)):
        print("Database not found, creating db...")
        if init_db.create_db(db_path):
            print("Database setup completed!")
        else:
            print("Oops! something happened, exiting script")
            return

    # Proceed with the main logic
    print("Starting main logic...")

    #####################################
    # Step 1: Download data from sources

    data_sources = load_sources(f"{current_dir}/sources.json")
    tmp_dir = f"{current_dir}/tmp/"

    if not Path.exists(Path(tmp_dir)):
        os.mkdir(tmp_dir)

    length = len(data_sources)
    for i, ds in enumerate(data_sources):
        print(f"Attempting CSV download {i+1}/{length}... ", end="")
        if download_csv(ds["url"], f"{tmp_dir}{ds['type']}.csv"):
            print("OK")

    #################################
    # Step 2: Store new data into DB

    for i, ds in enumerate(data_sources):
        print(f"Loading data into table {ds['type']}...", end="")
        res = insert_data(ds["type"], f"{tmp_dir}{ds['type']}.csv", db_path)
        if res:
            print("OK")
    print('-----')

    #######################
    # Step 3: Data queries

    get_total_revenue(db_path)
    print('-----')

    get_sales_by_product(db_path)
    print('-----')

    get_sales_by_region(db_path)
    print('-----')

if __name__ == "__main__":
    main()