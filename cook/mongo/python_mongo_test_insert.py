from pymongo_get_database import get_database
dbname = get_database()

# Create a new collection in the database called recipes
collection_name = dbname["recipes"]

