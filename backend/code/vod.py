from flask import Blueprint, request, jsonify
import requests
import json
import os
import hashlib
import base64

from config import base_url, api_token, org_id
import files

# Create a Blueprint object
vod_bp = Blueprint('vod', __name__)

UPLOAD_FOLDER = "/backend/code/assets"

headers = {
    "x-bv-org-id": org_id,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "authorization": "Bearer " + api_token,
}

def list_profile_set():
    url = base_url + "/bv/configuration/v1/profile-sets"
    querystring = {"current_page":"1","items_per_page":"1"}

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


@vod_bp.route('/create', methods=['GET'])
def create():
    if len(request.args) == 0:
        return jsonify({
            "code":"2",
            "message":"empty query string",
        }), 400
    if any(key not in ["video_name"] for key in request.args):
        return jsonify({
            "code":"3",
            "message":"invalid query keyword",
        }), 400
    
    video_name = request.args['video_name']
    vid = files.get_file_id(video_name)
    if vid == "" or len(vid) == 0:
        return jsonify({
            "code":"4",
            "message":"video not found in library",
        }), 400

    profile_set_id = list_profile_set()['profile_sets'][0]['id']

    payload = {
        "metadata": {
            "long_description": "it's just a test video to creat vod",
            "short_description": "test vod"
        },
        "name": video_name,
        "profile_set_id": profile_set_id,
        "pte": { "profile": "PTE_PROFILE_UNSPECIFIED" },
        "queue": "QUEUE_STANDARD",
        "security": {
            "domain_control": {
                "domains": ["https://showroom.one-dev.kkstream.io"],
                "enabled": False
            },
            "geo_control": [],
            "privacy": { "type": "SECURITY_PRIVACY_TYPE_PUBLIC" },
            "watermark": {
                "enabled": False,
                "position": "WATERMARK_POSITION_BOTTOM_RIGHT",
                "type": "WATERMARK_TYPE_IMAGE"
            }
        },
        "source": {
            "library": {
                "video": { "id":vid }
            },
            "type": "SOURCE_TYPE_LIBRARY"
        }
    }

    url = base_url + "/bv/cms/v1/vods"

    response = requests.post(url, json=payload, headers=headers)

    return response.json()