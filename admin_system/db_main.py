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