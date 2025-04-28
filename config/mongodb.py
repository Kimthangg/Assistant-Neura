"""
MongoDB Configuration for the chat application
"""

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "chatbot_db"
COLLECTION_NAME = "conversations"

# You can modify these settings as needed for your environment
# For production, consider using environment variables for sensitive values