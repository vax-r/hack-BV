from flask import Blueprint, request, jsonify, render_template
import requests
import json
import time
import multiprocessing

from config import base_url, api_token, org_id

# Create a Blueprint object
livestream_bp = Blueprint('livestream', __name__)

headers = {
    "x-bv-org-id": org_id,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "authorization": "Bearer " + api_token,
}

def get_live_id(livestream_name):
    url = base_url + "/bv/cms/v1/lives"

    querystring = {"current_page":"1","items_per_page":"1","filter.name":str(livestream_name)}

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()['lives'][0]['id']

# list all the livestream you have
@livestream_bp.route('/list', methods=['GET'])
def list():

    url = base_url + "/bv/cms/v1/lives"

    querystring = {"current_page":"1","items_per_page":"10"}

    response = requests.get(url, headers=headers, params=querystring)

    livestreams = []
    for live in response.json()['lives']:
        tmp = {}
        tmp['id'] = live['id']
        tmp['name'] = live['name']
        tmp['status'] = live['status']
        tmp['setup'] = live['setup']
        livestreams.append(tmp)

    if len(livestreams) == 0:
        return jsonify({
            "code":"1",
            "message":"No livestream",
        }), 200

    return str(livestreams)

def preview(live_id):
    # wait until the livestream is ready to be previewed
    getLive_url = base_url + "/bv/cms/v1/lives/" + live_id
    while True:
        getLive_res = requests.get(getLive_url, headers=headers)
        if getLive_res.json()['live']['status'] == "LIVE_STATUS_WAIT_FOR_PREVIEW":
            time.sleep(3)
            break
        time.sleep(30)

    # preview the livestream
    preview_url = base_url + "/bv/cms/v1/lives/" + str(live_id) + ":preview"
    payload = {}
    response = requests.post(preview_url, json=payload, headers=headers)
    print(response.json())
    return response.json()

# create a livestream
@livestream_bp.route('/create', methods=['GET'])
def create():

    if len(request.args) == 0 or any(key not in ["livestream_name"] for key in request.args):
        return jsonify({
            "code":"2",
            "message":"invalid query keyword",
        }), 400

    if request.args["livestream_name"] == "":
        return jsonify({
            "code":"3",
            "message":"invalid livestream name",
        }), 400
    
    create_url = base_url + "/bv/cms/v1/lives"

    payload = json.dumps({
    "live": {
        "broadcast_mode": "BROADCAST_MODE_TRADITIONAL_LIVE",
        "name": request.args["livestream_name"],
        "resolution": "LIVE_RESOLUTION_HD",
        "security": {
        "privacy": {
            "type": "SECURITY_PRIVACY_TYPE_PUBLIC"
        }
        },
        "type": "LIVE_TYPE_LIVE" # make other option here
    }
    })

    create_response = requests.request("POST", create_url, headers=headers, data=payload)
    if create_response.status_code != 200:
        return jsonify({
            "code":"4",
            "message":"Failed to create livestream",
            "error":create_response.text,
        }), 400
    
    livestream_id = create_response.json()['live']['id']

    # Preview the livestream
    multiprocessing.Process(target=preview, args=(
        str(livestream_id),
    )).start()
    
    # get livestream rtmp info
    get_url = base_url + "/bv/cms/v1/lives/" + str(livestream_id)
    response = requests.get(get_url, headers=headers)

    if response.status_code != 200:
        return jsonify({
            "code":"6",
            "message":"Failed to get info from livestream",
        }), 400
    
    rtmp_url = response.json()['live']['setup']['rtmp']['links'][0]['url']
    rtmp_key = response.json()['live']['setup']['rtmp']['links'][0]['stream_key']

    return jsonify({
        "code":"0",
        "message":"Create livestream successfully",
        "rtmp_url":rtmp_url,
        "rtmp_key":rtmp_key,
    }), 200

@livestream_bp.route('/get_rtmp', methods=['POST'])
def get_rtmp():
    if len(request.get_json()) == 0 or any(key not in ['livestream_id'] for key in request.get_json()):
        return jsonify({
            "code":"1",
            "message":"Invalid query keyword",
        }), 400  
    
    if request.get_json()["livestream_id"] == "":
        return jsonify({
            "code":"2",
            "message":"Invalid livestream id",
        }), 400
    
    livestream_id = request.get_json()["livestream_id"]

    url = base_url + "/bv/cms/v1/lives/" + str(livestream_id)
    response = requests.get(url, headers=headers)

    rtmp_url = response.json()['live']['setup']['rtmp']['links'][0]['url']
    rtmp_key = response.json()['live']['setup']['rtmp']['links'][0]['stream_key']

    return jsonify({
        "code":"0",
        "message":"Get livestream successfully",
        "rtmp_url":rtmp_url,
        "rtmp_key":rtmp_key,
    }), 200

# start your livestream
@livestream_bp.route('/start', methods=['POST'])
def start():
    url = base_url + "/bv/cms/v1/lives/" + request.get_json["livestream_id"] + ":start"
    payload = {}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return jsonify({
            "code":"1",
            "message":"Failed to start the livestream",
        }), response.status_code
    
    # TODO : broadcast the livestream's showroom url

    return jsonify({
        "code":"0",
        "message":"Start the livestream successfully",
    }), 200

# edit your livestream
@livestream_bp.route('/edit', methods=['POST'])
def edit():
    # TODO : write your code below
    return "edit"

# stop your livestream
@livestream_bp.route('/stop', methods=['GET'])
def stop():
    # TODO : write your code below
    return "stop"

@livestream_bp.route('/show', methods=['GET'])
def show():
    url = base_url + "/bv/cms/v1/lives"

    querystring = {"current_page":"1","items_per_page":"10"}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        return jsonify({
            "code","2",
            "message","error when listing livestreams",
        }), response.status_code
    
    livestreams = []
    for live in response.json()['lives']:
        tmp = {
            "name":live['name'],
            "id":live['id'],
            "status":live['status'],
        }
        livestreams.append(tmp)

    return render_template('livestream_list.html', livestreams = livestreams)