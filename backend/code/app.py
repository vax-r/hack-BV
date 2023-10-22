from flask import Flask, jsonify, request, render_template
import requests
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from cloud_storage import cloud_storage_bp
from files import file_bp
from livestream import livestream_bp
from vod import vod_bp
from config import base_url, api_token, org_id
from ai_helper import basic_chat

app = Flask(__name__)
app.register_blueprint(cloud_storage_bp, url_prefix='/cloud_storage')
app.register_blueprint(file_bp, url_prefix='/file')
app.register_blueprint(livestream_bp, url_prefix='/livestream')
app.register_blueprint(vod_bp, url_prefix='/vod')

socketio = SocketIO(app)

@app.route('/welcome', methods=['GET'])
def welcome():
    return "hello, world"

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('A user has connected.')

@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))

@socketio.on('send_message')
def send_message(data):
    user = data[0]
    message = data[1]

    emit('broadcast_message', [message, user], broadcast=True)
    if "teaching assistant" in message.lower() or "TA" in message:
        ans = basic_chat(message)
        emit('broadcast_message', [ans, "openAI TA"], broadcast=True)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, threaded=True, port='5000')
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)