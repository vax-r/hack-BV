from flask import Blueprint, request, jsonify
import requests
import json

# circular import needs future improvements
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
    # TODO : write your code below
    return "list"

# create a livestream
@livestream_bp.route('/create', methods=['GET', 'POST'])
def create():
    # TODO : write your code below
    return "create"

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