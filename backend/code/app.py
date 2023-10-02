from flask import Flask, jsonify, request
import requests
import json

from cloud_storage import cloud_storage_bp
from files import file_bp
from config import base_url, api_token, org_id

app = Flask(__name__)
app.register_blueprint(cloud_storage_bp, url_prefix='/cloud_storage')
app.register_blueprint(file_bp, url_prefix='/file')

@app.route('/welcome', methods=['GET'])
def welcome():
    return "hello, world"

# @app.route('/list_account', methods=['GET'])
# def list_account():
#     return

# list every files under your current account
# @app.route('/file_list', methods=['GET'])
# def list_files():
#     url = base_url + "/bv/cms/v1/library/files"
#     querystring = {"current_page":"1","items_per_page":"1","type":"FILE_TYPE_UNSPECIFIED"}
#     headers = {
#     "x-bv-org-id": org_id,
#     "Accept": "application/json",
#     "authorization": "Bearer " + api_token
#     }
#     response = requests.get(url, headers=headers, params=querystring)
#     return response.json()

# # list VODs
# @app.route('/list_VOD', methods=['GET'])
# def list_vod():
#     url = base_url + "/bv/cms/v1/vods"

#     querystring = {"current_page":"1","items_per_page":"1"}

#     headers = {
#         "x-bv-org-id": org_id,
#         "Accept": "application/json",
#         "authorization": "Bearer " + api_token
#     }

#     response = requests.get(url, headers=headers, params=querystring)

#     return response.json()['vods']

# # creat VOD
# @app.route('/vod_create', methods=['POST'])
# def vod_create():
#     url = base_url + "/bv/cms/v1/vods"

#     payload = {
#         "metadata": {
#             "long_description": "",
#             "short_description": ""
#         },
#         "name": "IMG_1882.MOV",
#         "profile_set_id": "6a2b2ea3-9e35-4216-93c9-da09dee5ab12",
#         "pte": { "profile": "PTE_PROFILE_UNSPECIFIED" },
#         "queue": "QUEUE_STANDARD",
#         "security": {
#             "domain_control": {
#                 "domains": ["https://showroom.one-dev.kkstream.io"],
#                 "enabled": False
#             },
#             "geo_control": [],
#             "privacy": { "type": "SECURITY_PRIVACY_TYPE_PUBLIC" },
#             "watermark": {
#                 "enabled": False,
#                 "position": "WATERMARK_POSITION_BOTTOM_RIGHT",
#                 "type": "WATERMARK_TYPE_IMAGE"
#             }
#         },
#         "source": {
#             "library": {
#                 "subtitles": [
#                     {
#                         "code": "eng",
#                         "display": "English",
#                         "id": "ff59095c-fd67-4edc-9705-5e56c31b3577",
#                         "name": "english.vtt"
#                     }
#                 ],
#                 "video": { "id": "c6f50caa-37ab-4d8c-9b06-e231544d598f" }
#             },
#             "type": "SOURCE_TYPE_LIBRARY"
#         }
#     }
#     headers = {
#         "x-bv-org-id": org_id,
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "authorization": "Bearer " + api_token
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     # print(response.json())
#     return response.json()

# @app.route('/file_upload', methods=['POST'])
# def file_upload():

#     url = base_url + "/bv/cms/v1/library/files:upload"

#     payload = { "file": {
#             "name": request.values['name'],
#             "size": request.values['size'],
#             "source": request.values['source'],
#             "type": request.values['type']
#         } }
#     headers = {
#         "x-bv-org-id": org_id,
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "authorization": "Bearer " + api_token
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     # print(response.json())
#     return response.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port='5000')