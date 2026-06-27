from pymongo import MongoClient
from pymongo.errors import PyMongoError

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        """
        Initializes the MongoClient and establishes connection with authentication.
        """
        # Connection Variables
        USER = username
        PASS = password
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'
        
        # Initialize Connection with authentication 
        try:
            self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource=admin')
            self.database = self.client[DB]
            self.collection = self.database[COL]
            print("Successfully connected to MongoDB.")
        except Exception as e:
            print(f"Error establishing connection to MongoDB database context: {e}")

    def create(self, data):
        """
        Inserts a document into the specified MongoDB collection.
        Input: data (dict containing key/value pairs)
        Output: True if successful insert, else False
        """
        if data is not None and isinstance(data, dict):
            try:
                # Execute the PyMongo driver insert API call
                insert_result = self.collection.insert_one(data)
                return insert_result.acknowledged
            except PyMongoError as e:
                print(f"Database insertion failed due to PyMongo error: {e}")
                return False
        else:
            # Enforce data type integrity constraints
            print("Create failed: Input data parameters must be provided in a dictionary format.")
            return False

    def read(self, query):
        """
        Queries for documents from the specified MongoDB collection.
        Input argument: query (dict containing key/value lookup pairs)
        Return: result in a list if successful, else an empty list
        """
        # Verify the query argument is in dictionary format
        if query is not None and isinstance(query, dict):
            try:
                # Execute find() to get a data cursor 
                cursor = self.collection.find(query)
                
                # Convert the MongoDB cursor stream directly into a standard Python list
                results_list = list(cursor)
                return results_list
            except Exception as e:
                print(f"An error occurred during the read operation: {e}")
                return []
        else:
            print("Read failed: Query parameter must be a valid dictionary.")
            return []

    def update(self, query, update_data):
        """
        Queries for and modifies documents matching the query parameter.
        Returns the integer count of modified documents.
        """
        if query is not None and update_data is not None and isinstance(query, dict) and isinstance(update_data, dict):
            try:
                # Uses the '$set' operator to modify fields safely without rewriting the record
                update_result = self.collection.update_many(query, {"$set": update_data})
                return update_result.modified_count
            except Exception as e:
                print(f"An error occurred during the update operation: {e}")
                return 0
        else:
            print("Update failed: Parameters must be non-empty dictionaries.")
            return 0

    def delete(self, query):
        """
        Queries for and removes documents matching the query parameter.
        Returns the integer count of removed documents.
        """
        if query is not None and isinstance(query, dict):
            try:
                # Removes targeted records securely from the collection
                delete_result = self.collection.delete_many(query)
                return delete_result.deleted_count
            except Exception as e:
                print(f"An error occurred during the delete operation: {e}")
                return 0
        else:
            print("Delete failed: Query parameter must be a valid dictionary.")
            return 0