import os
from dotenv import load_dotenv
from pymongo import MongoClient

def getDB():
    load_dotenv()
    client = MongoClient(os.getenv('MONGO_URI'))
    return client['gt_data']

if __name__ == "__main__":   
   dbname = getDB()