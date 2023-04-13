from pymongo.server_api import ServerApi
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
uri = "mongodb+srv://user:nJN5Z9JDXd7kmNy4@cluster0.bmg2rja.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['mydatabase']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# создаем коллекцию 'users'
users_collection = db['users']



@app.route('/')
def hello_world():
    return 'Hello, World!'


# определяем маршрут для получения списка пользователей
@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)


# определяем маршрут для создания нового пользователя
@app.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    user_count = users_collection.count_documents({})
    user['simple_id'] = user_count + 1
    result = users_collection.insert_one(user)
    print('Created user:', result.inserted_id)
    return jsonify({'inserted_id': str(result.inserted_id)})


@app.route('/users/<int:simple_id>', methods=['DELETE'])
def delete_user(simple_id):
    user = users_collection.find_one({'simple_id': simple_id})
    if user:
        result = users_collection.delete_one({'_id': user['_id']})
        if result.deleted_count == 1:
            return jsonify({'message': f'User with simple_id {simple_id} has been deleted'})
        else:
            return jsonify({'message': 'User not found'})
    else:
        return jsonify({'message': 'User not found'})


if __name__ == '__main__':
    app.run(debug=True)
