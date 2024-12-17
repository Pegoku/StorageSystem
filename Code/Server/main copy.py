from flask import Flask, request, json, Response
from flask_cors import CORS

import requests

import sqlite3


api = Flask(__name__)
CORS(api, resources={r"/*": {"origins": "*"}})
# api_list = [
# {
#     "name": "screw m3",
#     "description": "item1 description",
#     "category": "screw",
#     "quantity": 1,
#     "node": 1,
#     "position": 1,
#     "url": "url1"
# }, 
# {
#     "name": "screw m4",
#     "description": "item1 description",
#     "category": "screw",
#     "quantity": 1,
#     "node": 2,
#     "position": 2,
#     "url": "url1"
# }, 
# {
#     "name": "Tesa Tape",
#     "description": "item2 description",
#     "category": "tape",
#     "quantity": 5,
#     "node": 2,
#     "position": 3,
#     "url": "ima5555"
# }
# ]

# DB structure item, description, category, quantity, node, position, url (optional)


## Possible way: add to Storage table 16 slots and true if there, false if not. Messy but could work

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
        url TEXT,
        slot_1 BOOLEAN,
        slot_2 BOOLEAN,
        slot_3 BOOLEAN,
        slot_4 BOOLEAN,
        slot_5 BOOLEAN,
        slot_6 BOOLEAN,
        slot_7 BOOLEAN,
        slot_8 BOOLEAN,
        slot_9 BOOLEAN,
        slot_10 BOOLEAN,
        slot_11 BOOLEAN,
        slot_12 BOOLEAN,
        slot_13 BOOLEAN,
        slot_14 BOOLEAN,
        slot_15 BOOLEAN,
        slot_16 BOOLEAN)""")
    
    conn.commit()
    
    c.execute("""CREATE TABLE IF NOT EXISTS Nodes(
        id INTEGER PRIMARY KEY,
        ip TEXT,
        positions INTEGER)""")
    conn.commit()
    
    # c.execute("""CREATE TABLE IF NOT EXISTS listpositions(
    #     1 INTEGER,
    #     2 INTEGER,
    #     3 INTEGER,
    #     4 INTEGER,
    #     5 INTEGER,
    #     6 INTEGER,
    #     7 INTEGER,
    #     8 INTEGER,
    #     9 INTEGER,
    #     10 INTEGER,
    #     11 INTEGER,
    #     12 INTEGER,
    #     13 INTEGER,
    #     14 INTEGER,
    #     15 INTEGER,
    #     16 INTEGER""")
    # )
    conn.close()

def listStorage():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Storage")
    items = c.fetchall()
    conn.close()
    return items

def listNodes():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Nodes")
    items = c.fetchall()
    conn.close()
    return items

@api.route('/api/list', methods=['GET'])
def get_list():
    storage = listStorage()
    
    category = request.args.get('category')
    node = request.args.get('node')
    position = request.args.get('position')
    id = request.args.get('id')
    if category:
        storage = [item for item in storage if item[3] == category]
        # categories = [cat.strip() for cat in category.split(',')]
        # storage = [item for item in storage if item[3] in categories]
    if node:
        try:
            node = int(node)
            storage = [item for item in storage if item[5] == node]
        except ValueError:
            return json.jsonify({"error": "Invalid node value"})
    if position:
        try:
            position = int(position)
            storage = [item for item in storage if item[6] == position]
        except ValueError:
            return json.jsonify({"error": "Invalid position value"})
    if id:
        try:
            id = int(id)
            storage = [item for item in storage if item[0] == id]
        except ValueError:
            return json.jsonify({"error": "Invalid id value"})
    
        
    return json.jsonify(storage)

@api.route('/api/locateget', methods=['GET'])
def locate_get_item():
    # id = request.args.get('id')
    
    try:
        id = int(request.args.get('id'))
    except (TypeError, ValueError):
        return jsonify({"error": "id must be an integer"})

    
    if not id:
        return json.jsonify({"error": "id is required"})
    else:
        storage = listStorage()
        if not any(i[0] == id for i in storage):
            return json.jsonify({"error": "Item with id not found"})
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT node, position FROM Storage WHERE id = ?", (id,))
        location = c.fetchone()
        # conn.close()
        node = location[0]
        position = location[1]
        
        c.execute("SELECT ip FROM Nodes WHERE id = ?", (node,))
        ip = c.fetchone()[0]
        conn.close()
        
        url = "http://" + ip + ":4444/locate"
        
        payload = {"position": position}
        headers = {'Content-Type': 'application/json'}
        
        nodeResponse = requests.post(url, data=json.dumps(payload), headers=headers)

        if nodeResponse.status_code == 200:
            return json.jsonify({"success": True})
        else:
            return json.jsonify({"error": True})

@api.route('/api/additem', methods=['POST'])
def add_item():
    item = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    slots = [False] * 16
    slotsList = item['slots'] # [int(slot) for slot in item['slots'].split(',')] # Convert a, b, c, d to [a, b, c, d]
    for slot in slotsList:
        slots[int(slot) - 1] = True
    
    if 'name' not in item:
        return json.jsonify({"error": "name is required"})
    if 'description' not in item:
        return json.jsonify({"error": "description is required"})
    if 'category' not in item:
        return json.jsonify({"error": "category is required"})
    if 'quantity' not in item:
        return json.jsonify({"error": "quantity is required"})
    if 'node' not in item:
        return json.jsonify({"error": "node is required"})
    if 'position' not in item:
        return json.jsonify({"error": "position is required"})
    if 'slots' not in item:
        return json.jsonify({"error": "slots is required"})
    
    
    
    if item['url'] == '' or item['url'] == 'null' or 'url' not in item:
        item['url'] = None

    c.execute("INSERT INTO Storage (item, description, category, quantity, node, position, url, slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9, slot_10, slot_11, slot_12, slot_13, slot_14, slot_15, slot_16) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        (item['name'], item['description'], item['category'], item['quantity'], item['node'], item['position'], item['url'], *slots))
    conn.commit()
    conn.close()
    return json.jsonify({"success": True})

@api.route('/api/addnode', methods=['POST'])
def add_node():
    item = request.json
    if 'id' not in item:
        return json.jsonify({"error": "id is required"})
    if 'ip' not in item:
        return json.jsonify({"error": "ip is required"})
    if 'positions' not in item:
        return json.jsonify({"error": "positions is required"})
    try:
        item['id'] = int(item['id'])
        item['positions'] = int(item['positions'])
    except ValueError:
        return json.jsonify({"error": "Invalid id or positions value"})
    
    nodes = listNodes()
    
    if any(i[0] == item['id'] for i in nodes):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE Nodes set ip = ?, positions = ? WHERE id = ?", 
            (item['ip'], item['positions'], item['id']))
        conn.commit()
        conn.close()
        return json.jsonify({"error": "Item with id already exists, updated anyway"})
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Nodes (id, ip, positions) VALUES (?, ?, ?)", 
        (item['id'], item['ip'], item['positions']))
    conn.commit()
    conn.close()
    return json.jsonify({"success": True})

@api.route('/api/delete', methods=['POST'])
def delete_item():
    item = request.json
    if 'id' not in item:
        return json.jsonify({"error": "id is required"})
    else:
        storage = listStorage()
        if not any(i[0] == item['id'] for i in storage):
            return json.jsonify({"error": "Item with id not found"})
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM Storage WHERE id = ?", (item['id'],))
        conn.commit()
        conn.close()
        return json.jsonify({"success": True})

@api.route('/api/edit', methods=['POST'])
def edit_item():
    item = request.json
    if 'id' not in item:
        return json.jsonify({"error": "id is required"})
    else:
        storage = listStorage()
        if not any(i[0] == item['id'] for i in storage):
            return json.jsonify({"error": "Item with id not found"})
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE Storage SET item = ?, description = ?, category = ?, quantity = ?, node = ?, position = ?, url = ? WHERE id = ?", 
            (item['name'], item['description'], item['category'], item['quantity'], item['node'], item['position'], item['url'], item['id']))
        conn.commit()
        conn.close()
        return json.jsonify({"success": True})

@api.route('/api/quantity', methods=['POST'])
def quantity_item():
    item = request.json
    if 'id' not in item:
        return json.jsonify({"error": "id is required"})
    if 'quantity' not in item:
        return json.jsonify({"error": "quantity is required"})
    try:
        item['quantity'] = int(item['quantity'])
    except ValueError:
        return json.jsonify({"error": "Invalid quantity value"})
    else:
        storage = listStorage()
        if not any(i[0] == item['id'] for i in storage):
            return json.jsonify({"error": "Item with id not found"})
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE Storage SET quantity = ? WHERE id = ?", (item['quantity'], item['id']))
        conn.commit()
        conn.close()
        return json.jsonify({"success": True})

@api.route('/api/move', methods=['POST'])
def move_item():
    item = request
    if 'id' not in item:
        return json.jsonify({"error": "id is required"})
    if 'node' not in item:
        return json.jsonify({"error": "node is required"})
    if 'position' not in item:
        return json.jsonify({"error": "position is required"})
    try:
        item['node'] = int(item['node'])
        item['position'] = int(item['position'])
    except ValueError:
        return json.jsonify({"error": "Invalid node or position value"})
    else:
        storage = listStorage()
        if not any(i[0] == item['id'] for i in storage):
            return json.jsonify({"error": "Item with id not found"})
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE Storage SET node = ?, position = ? WHERE id = ?", (item['node'], item['position'], item['id']))
        conn.commit()
        conn.close()
        return json.jsonify({"success": True})
    
@api.route('/api/nodes', methods=['GET'])
def get_nodes():
    nodes = listNodes()
    
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
            nodes = [node for node in nodes if node[0] == id]
        except ValueError:
            return json.jsonify({"error": "Invalid id value"})
    return json.jsonify(nodes)

@api.route('/api/locate' , methods=['POST'])
def locate_item():
    item = request.json
    if 'id' not in item:
        return json.jsonify({"error": "id is required"})
    else:
        storage = listStorage()
        if not any(i[0] == item['id'] for i in storage):
            return json.jsonify({"error": "Item with id not found"})
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT node, position FROM Storage WHERE id = ?", (item['id'],))
        location = c.fetchone()
        # conn.close()
        node = location[0]
        position = location[1]
        
        c.execute("SELECT ip FROM Nodes WHERE id = ?", (node,))
        ip = c.fetchone()[0]
        conn.close()
        
        url = "http://" + ip + ":4444/locate"
        
        payload = {"position": position}
        headers = {'Content-Type': 'application/json'}
        
        nodeResponse = requests.post(url, data=json.dumps(payload), headers=headers)

        if nodeResponse.status_code == 200:
            return json.jsonify({"success": True})
        else:
            return json.jsonify({"error": True})
        # return json.jsonify({"node": location[0], "position": location[1]})

@api.route('/api/displaySlots', methods=['POST'])
def display_slots():
    item = requests.json
    if 'id' not in item:
        return json.jsonify({"error": "id is required"})
    

if __name__ == '__main__':
    init_db()
    api.run(debug=True, host='0.0.0.0', port=5000)