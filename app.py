from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://user:nJN5Z9JDXd7kmNy4@cluster0.bmg2rja.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)


@app.route('/')
def hello_world():
    # Get list of all database names on server
    db_list = client.list_database_names()
    return str(db_list)


if __name__ == '__main__':
    app.run()
