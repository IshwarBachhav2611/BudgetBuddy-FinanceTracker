from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["BudgetBuddy"]

activity_logs = db["activity_logs"]