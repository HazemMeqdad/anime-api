try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass
import os
from database import Database
from application import WitClient
import json

if not os.getenv("MONGODB_URL"):
    print("No `MONGODB_URL` set. Exiting...")
    exit(1)

database = Database(os.getenv("MONGODB_URL"))
wit = WitClient(database)

def main():
    database.connect()
    print("Connected to database")
    print("Starting...")
    result = wit.search_anime("One piece")

    espiodes = wit.get_espiodes(result[0]["page"])

    servers = wit.get_servers(espiodes[0]["watch_page"])

    print("Done!")

if __name__ == "__main__":
    main()
