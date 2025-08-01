import os
import sys
import uvicorn
from server.db.session import DB_FILE


def main():
    # Custom flag: --delete-db
    if "--delete-db" in sys.argv:
        if os.path.exists(DB_FILE):
            print(f"Deleting existing DB file: {DB_FILE}")
            os.remove(DB_FILE)
        sys.argv.remove("--delete-db")

    # Start the server
    uvicorn.run("server:app", host="0.0.0.0", port=8888, reload=True)


if __name__ == "__main__":
    main()
