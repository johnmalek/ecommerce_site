'''
Main CRUD a functions related to the database
'''
# import db connection variables
from .connections import *


# ADD ITEM ----------------------------------------------------------------------------

def add_item(collection_name: str, doc: dict) -> bool:
  '''
  add new item to the database collection
  
  Args:
    collection_name (str): collection you want to use
    doc (dict): document you are adding

  Return:
    True - if item was successfully added
    False - otherwise
  '''
  try:
    insert_doc = collection_name.insert_one(doc)
    doc_id = insert_doc.inserted_id
    return doc_id
  except Exception:
    print('Could not add item to database')


# FIND ITEM ---------------------------------------------------------------------------

def get_item_id(collection_name: str, item: str, item_name: str):
  '''
  get the item ID based on the item and item name (this should be chnaged based on your requirements) 

  Args:
    collection_name (str): collection you want to use
    item (str): the cetegory of the item
    item_name (str): name of the item
  
  Return:
    item ID
  '''
  try:
    item_found = collection_name.find_one({"item": item, "item_name": item_name})
    item_id = item_found['_id']
    return item_id
  except Exception:
    print('No items in dataase')
    return None


def find_all_items(collection_name: str):
  '''
  find all the items in the collection_name

  Args:
    collection_name (str): collection you want to use
  
  Return:
    list of all the items found
  '''
  try:
    all_items = list(collection_name.find())
    return all_items
  except Exception:
    print('No items in dataase')
    return None


def item_search(collection_name: str, index_name: str, index_path: str, query: str):
  '''
  strict search through collection_name

  This has to be set up in mongoDB atlas under the search tab

  Args:
    collection_name (str): collection you want to use
    index_name (str): name of the index you created on atlas
    index_path (str): the field your index is searching through, defined in atlas
    query (str): the 'search' you will submit

  Return 
    list of the items found
  '''
  
  try:
    result = collection_name.aggregate([
    {
      "$search":{
        "index": index_name,
        "text": {
          "query": query,
          "path": index_path
          }
        }
      }
    ])
    return list(result)
  except Exception:
    print('Could not find item in database')


def total_item_count(collection_name: str):
  '''
  count the total amount of elements in the collection specified

  Args:
    collection_name (str): the database collection we want to count
  
  Return:
    total items in collection
  '''
  try:
    count = collection_name.count_documents({})
    return count
  except Exception:
    print('Could not count collection')


# UPDATE ITEM ------------------------------------------------------------------------

def update_item_data(collection_name: str, item: str, item_name: str, doc: dict) -> bool:
  '''
  update item info

  Args:
    collection_name (str): collection you want to use
    item (str): the cetegory of the item
    item_name (str): name of the item
    doc (dict): doc with updated details

  Return:
    True - if item was successfully updated
    False - otherwise 
  '''
  item_id = get_item_id(collection_name, item, item_name)
  _id = ObjectId(item_id)
  updates = {
    "$set": doc
  }
  collection_name.update_one({"_id": _id}, updates)
  return _id


# DELETE ITEM -------------------------------------------------------------------------

def remove_item(collection_name: str, item: str, item_name: str) -> bool:
  '''
  delete a item

  Args:
    collection_name (str): collection you want to use
    item (str): the cetegory of the item
    item_name (str): name of the item

  Return:
    True - if item was successfully deleted
    False - otherwise
  '''
  item_id = get_item_id(collection_name, item, item_name)
  _id = ObjectId(item_id)
  collection_name.delete_one({"_id": _id})
  return _id
