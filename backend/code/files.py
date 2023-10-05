from flask import Blueprint, request, jsonify
import requests
import json
import os
import hashlib
import base64

from config import base_url, api_token, org_id

# Create a Blueprint object
file_bp = Blueprint('file', __name__)

UPLOAD_FOLDER = "/backend/code/assets"

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
        return response.json(), 200
    
    querystring["filter.name"] = request.args["video_name"] # query the requested video_name
    response = requests.get(url, headers=headers, params=querystring)
    return response.json(), 200

# search for specific file
@file_bp.route('/search/<video_name>', methods=['GET'])
def search(video_name):
    
    list_url = base_url + "/bv/cms/v1/library/files"
    querystring = {"current_page":"1","items_per_page":"5","type":"FILE_TYPE_VIDEO","filter.name":video_name}
    
    response = requests.get(list_url, headers=headers, params=querystring)
    
    file = response.json()["files"][0]
    search_url = base_url + "/bv/cms/v1/library/files/" + file["id"]

    response = requests.get(search_url, headers=headers)

    return response.json(), 200

def get_file_id(video_name):
    url = base_url + "/bv/cms/v1/library/files"
    querystring = {"current_page":"1","items_per_page":"1","type":"FILE_TYPE_VIDEO","filter.name":video_name}

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['files'][0]['id']

def sha1_digest(video_file_path):
    sha1 = hashlib.sha1()
    with open(video_file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read the file in 64KB chunks
            if not data:
                break
            sha1.update(data)

    sha1_hash = sha1.digest()
    base64_encoded_hash = base64.b64encode(sha1_hash).decode('utf-8')
    return base64_encoded_hash


# upload file
@file_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({
            "code":"2",
            "message":"No file part",
        }), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "code":"3",
            "message":"No selected file",
        }), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path) # store file in local

    # generate request for upload file
    url = base_url + "/bv/cms/v1/library/files:upload"

    payload = { "file": {
        "name": file.filename,
        "size": str(os.stat(file_path).st_size),
        "source": "FILE_SOURCE_UPLOAD_IN_LIBRARY",
        "type": "FILE_TYPE_VIDEO"
    } }

    response = requests.post(url, json=payload, headers=headers) # response of upload API

    fid = response.json()['file']['id']
    upload_id = response.json()['upload_data']['id']

    # generate checksum_sha1
    checksum_sha1 = sha1_digest(file_path)

    # generate body for complete upload
    parts = response.json()['upload_data']['parts']
    all_res = []
    i = 1
    for part in parts:
        with open(file_path, 'rb') as f:
            part_res = requests.put(part['presigned_url'], data=f)
            all_res.append({
                "etag": part_res.headers['ETag'],
                "part_number": i
            })
        i += 1

    # complete file upload url
    complete_url = base_url + "/bv/cms/v1/library/files/" + fid + ":complete-upload"
    payload = { "complete_data": {
        "checksum_sha1": checksum_sha1,
        "id": upload_id,
        "parts": all_res,
    } }

    response = requests.post(complete_url, json=payload, headers=headers)
    # print(response.json())
    if response.status_code != 200:
        return jsonify({
            "code":"400",
            "message":"file upload error",
            "message_from_BV":response.json(),
        }), response.status_code
    
    return jsonify({
        "code":"200",
        "message":"file upload successfully",
        "message_from_BV":response.json(),
    })