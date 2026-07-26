from datetime import datetime
from apps.mongodb import activity_logs


def log_activity(user, action, details=None):
    """
    Save user activity into MongoDB.
    """

    activity_logs.insert_one({
        "username": user.username,
        "user_id": user.id,
        "action": action,
        "details": details,
        "created_at": datetime.now(),
    })