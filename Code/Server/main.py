from flask import Flask, request, json, Response
import requests

import sqlite3


api = Flask(__name__)

# api_list = [
# {
#     "name": "screw m3",
#     "description": "item1 description",
#     "category": "screw",
#     "quantity": 1,
#     "node": 1,
#     "position": 1,
#     "image": "image1"
# }, 
# {
#     "name": "screw m4",
#     "description": "item1 description",
#     "category": "screw",
#     "quantity": 1,
#     "node": 2,
#     "position": 2,
#     "image": "image1"
# }, 
# {
#     "name": "Tesa Tape",
#     "description": "item2 description",
#     "category": "tape",
#     "quantity": 5,
#     "node": 2,
#     "position": 3,
#     "image": "ima5555"
# }
# ]

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
    
    c.execute("""CREATE TABLE IF NOT EXISTS Nodes(
        id INTEGER PRIMARY KEY,
        ip TEXT,
        slots INTEGER)""")
    conn.commit()
    
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
            return json.jsonify({"error": "Invalid node value"})
        
    return json.jsonify(storage)

@api.route('/api/additem', methods=['POST'])
def add_item():
    item = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Storage (item, description, category, quantity, node , position, image) VALUES (?, ?, ?, ?, ?, ?, ?)", 
        (item['name'], item['description'], item['category'], item['quantity'], item['node'], item['position'], item['image']))
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
    if 'slots' not in item:
        return json.jsonify({"error": "slots is required"})
    try:
        item['id'] = int(item['id'])
        item['slots'] = int(item['slots'])
    except ValueError:
        return json.jsonify({"error": "Invalid id or slots value"})
    
    nodes = listNodes()
    
    if any(i[0] == item['id'] for i in nodes):
        return json.jsonify({"error": "Item with id already exists"})
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Nodes (id, ip, slots) VALUES (?, ?, ?)", 
        (item['id'], item['ip'], item['slots']))
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
        c.execute("UPDATE Storage SET item = ?, description = ?, category = ?, quantity = ?, node = ?, position = ?, image = ? WHERE id = ?", 
            (item['name'], item['description'], item['category'], item['quantity'], item['node'], item['position'], item['image'], item['id']))
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
        
        payload = {"slot": position}
        headers = {'Content-Type': 'application/json'}
        
        nodeResponse = requests.post(url, data=json.dumps(payload), headers=headers)

        if nodeResponse.status_code == 200:
            return Response("Success", mimetype='text/plain')
        else:
            return Response("Error", mimetype='text/plain')
        # return json.jsonify({"node": location[0], "position": location[1]})

if __name__ == '__main__':
    init_db()
    api.run(debug=True, host='0.0.0.0', port=5000)