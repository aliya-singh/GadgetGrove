import json
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from bson import ObjectId
from datetime import datetime
import time

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "gadgetgrove")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "reviews")

def get_mongo_connection(retries=5, delay=2):
    """Establish MongoDB connection with timeout and retries"""
    for attempt in range(retries):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
            # Verify connection is working
            client.admin.command('ping')
            db = client[MONGO_DB]
            collection = db[MONGO_COLLECTION]
            return client, db, collection
        except Exception as e:
            if attempt < retries - 1:
                print(f"MongoDB connection attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise ConnectionError(f"Failed to connect to MongoDB at {MONGO_URI} after {retries} attempts: {str(e)}")


def get_reviews(as_json_safe=True):
    try:
        client, db, collection = get_mongo_connection()
        reviews = list(collection.find({}))
        client.close()
        
        if as_json_safe:
            # Convert ObjectIds to strings for JSON compatibility
            for review in reviews:
                if '_id' in review:
                    review['_id'] = str(review['_id'])
        
        return reviews
    except Exception as e:
        raise Exception(f"Failed to retrieve reviews from MongoDB: {str(e)}")

def setup_nosql_data(file_name="data/mongo_reviews.json"):
    reviews = [
        {"review_id": 1, "product_id": 101, "customer_id": 1, "rating": 5, "review_text": "Amazing watch!"},
        {"review_id": 2, "product_id": 102, "customer_id": 2, "rating": 4, "review_text": "Great sound quality."},
        {"review_id": 3, "product_id": 103, "customer_id": 1, "rating": 5, "review_text": "Perfect for work."},
        {"review_id": 4, "product_id": 101, "customer_id": 3, "rating": 2, "review_text": "Too small for my wrist."},
        {"review_id": 5, "product_id": 105, "customer_id": 4, "rating": 5, "review_text": "Best phone ever."},
        {"review_id": 6, "product_id": 104, "customer_id": 5, "rating": 3, "review_text": "Keyboard is okay, a bit loud."},
        {"review_id": 7, "product_id": 101, "customer_id": 2, "rating": 4, "review_text": "Stylish and functional."},
        {"review_id": 8, "product_id": 102, "customer_id": 6, "rating": 5, "review_text": "Immersive audio experience."},
        {"review_id": 9, "product_id": 103, "customer_id": 7, "rating": 1, "review_text": "Screen cracked after a week."},
        {"review_id": 10, "product_id": 105, "customer_id": 8, "rating": 4, "review_text": "Great camera."},
        {"review_id": 11, "product_id": 101, "customer_id": 9, "rating": 5, "review_text": "Love the fitness features."},
        {"review_id": 12, "product_id": 102, "customer_id": 10, "rating": 3, "review_text": "Average headphones."},
        {"review_id": 13, "product_id": 105, "customer_id": 1, "rating": 5, "review_text": "Second purchase, still loving it."},
        {"review_id": 14, "product_id": 102, "customer_id": 3, "rating": 4, "review_text": "Good value for money."},
        {"review_id": 15, "product_id": 104, "customer_id": 4, "rating": 2, "review_text": "Keys stuck after a month."}
    ]
    
    try:
        # Connect to MongoDB
        client, db, collection = get_mongo_connection()
        
        # Clear existing reviews
        collection.delete_many({})
        
        # Insert reviews into MongoDB
        result = collection.insert_many(reviews)
        inserted_count = len(result.inserted_ids)
        
        # Backup to JSON file (handle ObjectIds and datetime)
        try:
            with open(file_name, 'w') as f:
                json.dump(reviews, f, indent=4, cls=MongoJSONEncoder)
        except Exception as backup_error:
            # Log backup error but don't fail the setup
            print(f"Warning: Could not backup to JSON file: {str(backup_error)}")
        
        client.close()
        
        return f"MongoDB initialized with {inserted_count} reviews in database '{MONGO_DB}', collection '{MONGO_COLLECTION}'."
    except Exception as e:
        return f"Error setting up MongoDB: {str(e)}"