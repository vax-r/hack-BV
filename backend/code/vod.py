from flask import Blueprint, request, jsonify, render_template
import requests
import json
import os
import hashlib
import base64
import datetime

from config import base_url, api_token, org_id
import files

# Create a Blueprint object
vod_bp = Blueprint('vod', __name__)

UPLOAD_FOLDER = "/backend/code/assets"

SHOWROOM_URL = "https://showroom.one-stage.kkstream.io/embed?token="

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

    if response.status_code != 200:
        return jsonify({
            "code":"5",
            "message":"error when creating VOD",
            "message_from_BV":response.json(),
        }), 400

    # Notify linebot to broadcast the VOD to every users
    url = "http://go-linebot:8080/broadcast"
    params = {
        "vod_name":response.json()['vod']['name'],
        "vod_url":SHOWROOM_URL + get_rtoken(response.json()['vod']['id'])
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({
            "code":"6",
            "message":"failed to broadcast through linebot",
        }), 400

    return jsonify({
        "code":"0",
        "message":"VOD created successfully"
    }), 200

# There's a bug
@vod_bp.route('/analytic', methods=['GET'])
def analytic():

    url = base_url + "/bv/analytics/v1/reports/watch-time"

    querystring = {"time":datetime.datetime.now().isoformat(), "streaming_type":"REPORT_STREAMING_TYPE_UNSPECIFIED"}

    response = requests.get(url, headers=headers, params=querystring)    

    if response.status_code != 200:
        return jsonify({
            "code":"3",
            "message":response.text,
        }), 400

    return response.json()

# Get resource token of VOD
def get_rtoken(rid):

    url = base_url + "/bv/cms/v1/resources/tokens"

    payload = {
        "resource_id": rid,
        "resource_type": "RESOURCE_TYPE_VOD",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return "null"

    return response.json()['token']


# List all the important info of VODs
@vod_bp.route('/list', methods=['GET'])
def list():
    url = base_url + "/bv/cms/v1/vods"

    querystring = {"current_page":"1","items_per_page":"10"}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        return jsonify({
            "code":"3",
            "message":"Error when listing vods",
        }), 400
    
    vods = []
    for vod in response.json()['vods']:
        if vod['status'] != "VOD_STATUS_SUCCEEDED":
            continue
        tmp = {}
        tmp['name'] = vod['name']
        tmp['id'] = vod['id']
        tmp['showroom_url'] = SHOWROOM_URL + get_rtoken(vod['id'])
        vods.append(tmp)

    return jsonify({
        "code":"0",
        "message":"Successfully get all vods info",
        "data":vods,
    }), 200

# VOD wall for all VODs
@vod_bp.route('/show')
def show():
    url = base_url + "/bv/cms/v1/vods"

    querystring = {"current_page":"1","items_per_page":"10"}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        return jsonify({
            "code":"3",
            "message":"Error when listing vods",
        }), 400
    
    urls = []
    for vod in response.json()['vods']:
        if vod['status'] != "VOD_STATUS_SUCCEEDED":
            continue
        urls.append(SHOWROOM_URL + get_rtoken(vod['id']))

    return render_template('vod_list.html', video_urls = urls)