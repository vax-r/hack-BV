from flask import Blueprint, request, jsonify
import requests
import json

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
    querystring = {"current_page":"1","items_per_page":"1"}

    response = requests.get(url, headers=headers, params=querystring)

    
    return response.json()

# create a livestream
@livestream_bp.route('/create', methods=['GET', 'POST'])
def create():
    url = base_url + "/bv/cms/v1/lives/{id}:start"
   



    payload = {}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
    return "create"
    
    

# edit your livestream
@livestream_bp.route('/edit', methods=['POST'])
def edit():
    # TODO :
    #  write your code below
    return "edit"

# stop your livestream
@livestream_bp.route('/stop', methods=['GET'])
def stop():
    # TODO : write your code below
    url = base_url + "/bv/cms/v1/library/files"

    response = requests.delete(url, headers=headers)

    print(response.json())
    return response.json()