from import_data import load_sources, download_csv, insert_data
from pathlib import Path
import argparse
import init_db
import os


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
        if download_csv(ds["url"], f"{tmp_dir}{ds["type"]}.csv"):
            print("OK")

    #################################
    # Step 2: Store new data into DB

    for i, ds in enumerate(data_sources):
        print(f"Loading data into table {ds['type']}...", end="")
        insert_data(ds["type"], f"{tmp_dir}{ds["type"]}.csv", db_path)
        print("OK")


if __name__ == "__main__":
    main()