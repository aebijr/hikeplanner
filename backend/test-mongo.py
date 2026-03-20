import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

if not uri:
    print("Fehler: MONGODB_URI nicht gefunden")
    raise SystemExit(1)

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("Verbindung erfolgreich")
except Exception as e:
    print("Verbindung fehlgeschlagen:")
    print(e)