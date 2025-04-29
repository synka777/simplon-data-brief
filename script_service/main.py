from pathlib import Path
import argparse
import requests
import init_db
import json
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Script with optional --dev flag")
    parser.add_argument('--dev', action='store_true', help='Run in dev mode')
    return parser.parse_args()


def download_csv(url, dest):
    response = requests.get(url)

    if response.status_code == 200:
        # Will overwrite the old csv files with updated ones next time it runs
        with open(dest, 'wb') as file:
            file.write(response.content)
        return True
    else:
        print(f"\nFailed to download the file. Status code: {response.status_code}")
        return False


def load_sources(json_path):
    with open(json_path) as j:
        return json.load(j)


def main():
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    db_path = "/data/databrief.db" # Default: production (shared volume path)

    args = parse_args()
    if args.dev:
        print("Running in development mode")
        db_path = f"{parent_dir}/shared_data/databrief.db"

    if not Path.exists(Path(db_path)):
        print("Database not found, creating db...")
        if init_db.create_db(db_path):
            print("Database setup completed!")
        else:
            print('Oops! something happened, exiting script')
            return

    # Proceed with the main logic
    print("Starting main logic...")
    data_sources = load_sources(f"{current_dir}/sources.json")
    tmp_dir = f"{current_dir}/tmp/"

    if not Path.exists(Path(tmp_dir)):
        os.mkdir(tmp_dir)

    length = len(data_sources)
    for i, ds in enumerate(data_sources):
        print(f"Attempting CSV download {i+1}/{length}... ", end="")
        if download_csv(ds["url"], f"{tmp_dir}{ds["type"]}.csv"):
            print('OK')


if __name__ == '__main__':
    main()