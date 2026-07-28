import os

from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from .env
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

# Use the BudgetBuddy database
db = client["BudgetBuddy"]

# Activity Logs Collection
activity_logs = db["activity_logs"]