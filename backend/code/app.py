from flask import Flask, jsonify, request, render_template
import requests
import json

from cloud_storage import cloud_storage_bp
from files import file_bp
from livestream import livestream_bp
from config import base_url, api_token, org_id

app = Flask(__name__)
app.register_blueprint(cloud_storage_bp, url_prefix='/cloud_storage')
app.register_blueprint(file_bp, url_prefix='/file')
app.register_blueprint(livestream_bp, url_prefix='/livestream')

@app.route('/welcome', methods=['GET'])
def welcome():
    return "hello, world"

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port='5000')