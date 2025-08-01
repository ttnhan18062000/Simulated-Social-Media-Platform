import asyncio
import os
import sys
import uvicorn

from server.db.session import DB_FILE
from scripts.init_data import seed


def main():
    # Parse flags
    init_db_flag = "--init-db" in sys.argv
    init_data_flag = "--init-data" in sys.argv

    # Clean flags from sys.argv so uvicorn doesn't choke
    for flag in ("--init-db", "--init-data"):
        if flag in sys.argv:
            sys.argv.remove(flag)

    # Delete the database file if either flag is set
    if init_db_flag or init_data_flag:
        if os.path.exists(DB_FILE):
            print(f"🗑️  Deleting existing DB file: {DB_FILE}")
            os.remove(DB_FILE)

    # Run seeding if --init-data
    if init_data_flag:
        print("🌱 Seeding database with test data...")
        asyncio.run(seed())

    # Start the FastAPI server
    print("🚀 Starting FastAPI server...")
    uvicorn.run("server:app", host="0.0.0.0", port=8888, reload=True)


if __name__ == "__main__":
    main()
