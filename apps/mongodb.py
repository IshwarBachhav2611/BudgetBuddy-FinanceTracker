import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)

db = client["BudgetBuddy"]
activity_logs = db["activity_logs"]