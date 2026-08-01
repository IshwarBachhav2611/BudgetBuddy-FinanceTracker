import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the MongoDB connection string from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Create a MongoDB client with a 5-second server selection timeout
# This prevents the application from hanging indefinitely if the
# MongoDB server is unreachable.
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

# Verify that the MongoDB server is reachable
# Prints a success or failure message during application startup.
try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)

# Access the BudgetBuddy database
db = client["BudgetBuddy"]

# Reference the activity_logs collection
activity_logs = db["activity_logs"]