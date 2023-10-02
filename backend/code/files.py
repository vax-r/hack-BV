from flask import Blueprint, request, jsonify
import requests
import json

# circular import needs future improvements
from config import base_url, api_token, org_id

# Create a Blueprint object
file_bp = Blueprint('file', __name__)

headers = {
    "x-bv-org-id": org_id,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "authorization": "Bearer " + api_token,
}

# list videos under library/video
@file_bp.route('/list', methods=['GET'])
def list():
    url = base_url + "/bv/cms/v1/library/files"
    querystring = {"current_page":"1","items_per_page":"10","type":"FILE_TYPE_VIDEO"}
    
    if len(request.args) != 0 and any(key not in ['video_name'] for key in request.args):
        return jsonify({
            "code":"2",
            "message":"invalid arguments",
        }), 400
    elif len(request.args) == 0:
        # if no specify video name, then return all the files
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    
    querystring["filter.name"] = request.args["video_name"] # query the requested video_name
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# search for specific file
@file_bp.route('/search/<video_name>', methods=['GET'])
def search(video_name):
    
    list_url = base_url + "/bv/cms/v1/library/files"
    querystring = {"current_page":"1","items_per_page":"5","type":"FILE_TYPE_VIDEO","filter.name":video_name}
    
    response = requests.get(list_url, headers=headers, params=querystring)
    
    file = response.json()["files"][0]
    search_url = base_url + "/bv/cms/v1/library/files/" + file["id"]

    response = requests.get(search_url, headers=headers)

    return response.json()
