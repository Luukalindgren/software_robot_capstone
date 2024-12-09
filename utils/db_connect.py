from pymongo import MongoClient
from config import load_environment_variables
from data_from_excel import get_user_data
import os

def connect_to_db():
    try:
        load_environment_variables()
        mongo_url = os.getenv("MONGODB_URL")

        client = MongoClient(mongo_url)

        print("Connected to MongoDB")
        return client
    
    except Exception as e:
        print("Error connecting to MongoDB: ", e)
        return None
    

def upload_sessions_to_db(client):
    sessions_dir = 'temp'
    try:
        db = client["Testing_by_Luuka"]
        print("Uploading sessions to MongoDB...")

        for filename in os.listdir(sessions_dir):
            full_path = os.path.join(sessions_dir, filename)
            print("Uploading file:", full_path)
            if os.path.isfile(full_path):
                user_data = get_user_data(full_path)
                collection_name = db[filename.replace(".xlsx", "")]
                iteration = 0
                for user in user_data:
                    filter_query = {'user_id': user_data[iteration]['user_id']}
                    update_data = {"$set": user_data[iteration]}
                    collection_name.update_one(filter_query, update_data, upsert=True)
                    iteration += 1

        print("Sessions uploaded to MongoDB")
    except Exception as e:
        print("Error uploading sessions to MongoDB: ", e)

def main():
    client = connect_to_db()
    upload_sessions_to_db(client)
    client.close()

if __name__ == "__main__":
    main()