'''
Used to include all connection setup for the app
- database connection
- payment connection
'''

'''General imports'''
# access environment variables
import os
from dotenv import load_dotenv

load_dotenv()

'''MongoDB imports'''
# Connect MongoDB (quick start modules)
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# working with MongoDB's ObjectIDs.
from bson.objectid import ObjectId
from bson import Binary
import base64

'''Stripe imports'''
# Allow CRUD operations and payments method

'''Email imports'''
from email.message import EmailMessage
import ssl
import smtplib

# DATABASE CONNECTIONS --------------------------------------------------------------------------
# Create a new client and connect to the server
uri = os.environ["MONGO_URI"] # store connection string into environment varibale MONGO_URI
client = MongoClient(uri, server_api=ServerApi('1'))

# Define database
database_name = "ecommerce"
db = client[database_name]

# Define database collections
collection_name_1 = "products"
collection_name_2 = "users"
collection_name_3 = "insert_name_of_collection"
collection_name_4 = "insert_name_of_collection"
collection_name_5 = "insert_name_of_collection"

collection_1 = db[collection_name_1]
collection_2 = db[collection_name_2]
collection_3 = db[collection_name_3]
collection_4 = db[collection_name_4]
collection_5 = db[collection_name_5]

def testing_db_conenction():
  '''
  Send a ping to confirm a successful connection
  '''
  try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
    print(e)


# EMAIL CONNECTION -------------------------------------------------------------------------------

# Connect to email address
# email_sender = os.environ['EMAIL_SENDER']
# email_password = os.environ['EMAIL_PASSWORD']

# variable to configure email
em = EmailMessage()
context = ssl.create_default_context()
