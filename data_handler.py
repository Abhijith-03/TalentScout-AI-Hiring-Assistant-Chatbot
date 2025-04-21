import json
import uuid
from pymongo import MongoClient

# MongoDB Connection Setup
MONGO_URI = "mongodb+srv://jagdeesh:porr7214@talentscoutai.e2mx2.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true&appName=TalentScoutAI"
# Update with actual MongoDB URI if needed
DB_NAME = "TalentScout"
COLLECTION_NAME = "Candidates"

# Ensure MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_candidate_data(candidate_data):
    """
    Saves candidate data securely in MongoDB, ensuring no local file storage.
    """
    # Generate a unique ID for the candidate
    file_id = str(uuid.uuid4())[:8]  # Shortened UUID for readability
    candidate_data["File ID"] = file_id  # Store the unique file ID in data

    # Save data securely in MongoDB
    try:
        collection.insert_one(candidate_data)
        print(f" Data securely stored in MongoDB under {DB_NAME}.{COLLECTION_NAME}")
    except Exception as e:
        print(f" Error saving to MongoDB: {e}")

def load_candidate_data(file_id):
    """
    Loads candidate data securely from MongoDB using the unique file ID.
    """
    candidate_data = collection.find_one({"File ID": file_id}, {"_id": 0})  # Exclude MongoDB ObjectId
    if candidate_data:
        return candidate_data

    print(f" No data found with File ID: {file_id}")
    return None

def list_all_candidates():
    """
    Lists all saved candidates from MongoDB.
    """
    candidates = collection.find({}, {"full_name": 1, "File ID": 1, "_id": 0})
    return [{"Name": c["full_name"], "File ID": c["File ID"]} for c in candidates]
