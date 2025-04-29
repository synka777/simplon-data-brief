from pathlib import Path
import argparse
import init_db


def parse_args():
    parser = argparse.ArgumentParser(description="Script with optional --dev flag")
    parser.add_argument('--dev', action='store_true', help='Run in dev mode')
    return parser.parse_args()


def main():
    parent_dir = Path(__file__).resolve().parent.parent
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




if __name__ == '__main__':
    main()