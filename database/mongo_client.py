import pymongo
from pymongo import MongoClient
from config.settings import (
    MONGO_USER, 
    MONGO_PASSWORD, 
    MONGO_DATABASE, 
    MONGO_HOST, 
    MONGO_PORT
)

def connect_to_mongodb():
    """
    Connects to a MongoDB database.

    Returns:
        pymongo.database.Database: A MongoDB database object if the connection is successful,
                                  or None if there's an error.
        str: An error message if the connection fails, or None if successful.
    """
    try:
        uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}?authSource={MONGO_DATABASE}"
        print(uri)
        client = MongoClient(uri)

        client.admin.command('ping')
        print("Successfully connected to MongoDB!")

        db = client[MONGO_DATABASE]
        return db, None

    except pymongo.errors.ConnectionFailure as e:
        error_message = f"Could not connect to MongoDB: {e}"
        print(error_message)
        return None, error_message
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return None, error_message


# Optional: Keep this for testing the connection
if __name__ == "__main__":
    db, error = connect_to_mongodb()

    if error:
        print(f"Connection failed: {error}")
        quit()

    # Test insertion
    collection = db["HelloWorld"]
    document = {"name": "Test Document", "value": 123}
    inserted_document = collection.insert_one(document)
    print(f"Inserted document ID: {inserted_document.inserted_id}")

    # Test retrieval
    found_document = collection.find_one({"name": "Test Document"})
    print(f"Found document: {found_document}")
    db.client.close()
    