from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (you can replace this with your own data or database)
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]

@app.route('/welcome', methods=['GET'])
def welcome():
    return "hello, world"

# Endpoint to get a list of all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({"items": items})

# Endpoint to get information about a specific item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is not None:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port='5000')