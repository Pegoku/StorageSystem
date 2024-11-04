from flask import Flask, request, json

import sqlite3


api = Flask(__name__)

api_list = [
{
    "name": "screw m3",
    "description": "item1 description",
    "category": "screw",
    "quantity": 1,
    "node": 1,
    "position": 1,
    "image": "image1"
}, 
{
    "name": "screw m4",
    "description": "item1 description",
    "category": "screw",
    "quantity": 1,
    "node": 2,
    "position": 2,
    "image": "image1"
}, 
{
    "name": "Tesa Tape",
    "description": "item2 description",
    "category": "tape",
    "quantity": 5,
    "node": 2,
    "position": 3,
    "image": "ima5555"
}
]
# DB structure item, description, category, quantity, node, position, image (optional)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Storage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        description TEXT,
        category TEXT,
        quantity INTEGER,
        node INTEGER,
        position INTEGER,
        image TEXT)""")

    conn.commit()
    conn.close()

def listStorage():
    return api_list

@api.route('/api/list', methods=['GET'])
def get_list():
    storage = listStorage()
    
    category = request.args.get('category')
    node = request.args.get('node')
    position = request.args.get('position')
    
    if category:
        storage = [item for item in storage if item['category'] == category]
    if node:
        try:
            node = int(node)
            storage = [item for item in storage if item['node'] == node]
        except ValueError:
            return json.jsonify({"error": "Invalid node value"})
    if position:
        try:
            position = int(position)
            storage = [item for item in storage if item['position'] == position]
        except ValueError:
            return json.jsonify({"error": "Invalid node value"})
        
    return json.jsonify(storage)

    # return json.jsonify(listStorage)

if __name__ == '__main__':
    init_db()
    api.run(debug=True)