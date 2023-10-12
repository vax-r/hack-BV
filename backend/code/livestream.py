from flask import Blueprint, request, jsonify
import requests
import json
import time

from config import base_url, api_token, org_id

# Create a Blueprint object
livestream_bp = Blueprint('livestream', __name__)

headers = {
    "x-bv-org-id": org_id,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "authorization": "Bearer " + api_token,
}

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
        livestreams.append(tmp)

    if len(livestreams) == 0:
        return jsonify({
            "code":"1",
            "message":"No livestream",
        }), 200

    return str(livestreams)

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


    # KKcompany seems to have issues with the following APIs

    # wait until the livestream is ready to be previewed
    # getLive_url = base_url + "/bv/cms/v1/lives/" + livestream_id
    # while True:
    #     getLive_res = requests.get(getLive_url, headers=headers)
    #     if getLive_res.json()['live']['status'] == "LIVE_STATUS_WAIT_FOR_PREVIEW":
    #         break
    #     time.sleep(30)

    # # preview the livestream
    # preview_url = base_url + "/bv/cms/v1/lives/" + livestream_id + ":preview"
    # response = requests.post(preview_url, json=payload, headers=headers)

    # return response.json()

    return jsonify({
        "code":"0",
        "message":"Create livestream successfully",
    }), 200

@livestream_bp.route('/preview', methods=['POST'])
def preview():

    if len(request.values) == 0 or any(key not in ["livestream_id"] for key in request.values):
        return jsonify({
            "code":"2",
            "message":"invalid query keyword",
        }), 400

    if request.values["livestream_id"] == "":
        return jsonify({
            "code":"3",
            "message":"invalid livestream id",
        }), 400


    return jsonify({
        "code":"0",
        "message":"Preview livestream successfully",
        "id":request.values["livestream_id"],
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