'''
Used to include all connection setup for the app
- database connection
- email connection
'''

'''General imports'''
# access environment variables
import os

'''MongoDB imports'''
# Connect MongoDB (quick start modules)
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# working with MongoDB's ObjectIDs.
from bson.objectid import ObjectId


# DATABASE CONNECTIONS --------------------------------------------------------------------------
# Create a new client and connect to the server
uri = os.environ['MONGO_URI'] # store connection string into environment varibale MONGO_URI
client = MongoClient(uri, server_api=ServerApi('1'))

# Define database
database_name = "admin_system"
db = client[database_name]

# Define database collections
collection_1 = db["employees"]
collection_2 = db["departments"]


def testing_db_conenction():
  '''
  Send a ping to confirm a successful connection
  '''
  try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
    print(e)
