from flask import Flask, request
import pymongo
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin

client = pymongo.MongoClient(
    "mongodb+srv://nine:root@nine-nfire.f9yn8.mongodb.net/contacts_flask_rest?retryWrites=true&w=majority")
db = client['contacts_flask_rest']
col = db['contacts']

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def contacts():
    return 'Flask Contacts API'


@app.route('/contacts')
@cross_origin()
def get_contacts():
    contacts = col.find().sort('name')
    contacts = [{'_id': str(contact['_id']),
                 "name": contact['name'],
                 "email": contact['email'],
                 'number': contact['number']}
                for contact in
                contacts]
    return {"contacts": contacts}


@app.route('/contacts/<id>')
@cross_origin()
def get_contact(id):
    if not ObjectId.is_valid(id):
        return {"message": "Invalid ID"}
    contact = {"_id": ObjectId(id)}
    find = col.find_one(contact)
    if find is None:
        return {"error": "contact not found"}
    return {'_id': str(contact['_id']), 'name': find['name'], 'number': find['number'], 'email': find['email']}


@app.route('/contacts', methods=["POST"])
@cross_origin()
def add_contact():
    contact = {
        "name": request.json['name'],
        "number": request.json['number'],
        "email": request.json['email']
    }

    col.insert_one(contact)
    return {'message': 'contact created'}


@app.route('/contacts', methods=["PUT"])
@cross_origin()
def update_contact():
    id = request.json['_id']
    if not ObjectId.is_valid(id):
        return {"message": "Invalid ID"}
    to_update = {
        '_id': ObjectId(id)
    }
    values = {'$set': {
        "name": request.json['name'],
        "email": request.json['email'],
        "number": request.json['number']
    }}
    col.update_one(to_update, values)
    return {'message': "contact updated"}


@app.route('/contacts/<id>', methods=['DELETE'])
@cross_origin()
def delete_contact(id):
    to_delete = {
        '_id': ObjectId(id)
    }
    col.delete_one(to_delete)
    return {'message': "contact deleted"}


if __name__ == '__main__':
    app.run(debug=True)
