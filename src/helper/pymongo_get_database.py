from pymongo import MongoClient


def get_database():

   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   client = MongoClient(
       "mongodb+srv://adityapawar:npQbnHyKUVyzNFLf@cluster0.sh02b40.mongodb.net/?retryWrites=true&w=majority")
       
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['cookbook']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

   # Get the database
   dbname = get_database()
