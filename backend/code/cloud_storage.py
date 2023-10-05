# This file manages all operations related to cloud storages

from flask import Blueprint
import requests

from config import base_url, api_token, org_id

# Create a Blueprint object
cloud_storage_bp = Blueprint('cloud_storage', __name__)

headers = {
    "x-bv-org-id": org_id,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "authorization": "Bearer " + api_token,
}

# tp = dict()

# get trust policy
@cloud_storage_bp.route('/trust-policy', methods=['GET'])
def trust_policy():
    url = base_url + "/bv/configuration/v1/cloud-storages/trust-policy"
    response = requests.get(url, headers=headers)
    return response.json()

# create cloud storage
# aws path not found
@cloud_storage_bp.route('/create', methods=['POST'])
def create():
    url = base_url + "/bv/configuration/v1/cloud-storages"
    tp = trust_policy() # get trust policy of aws

    payload = { "cloud_storage": {
            "aws_storage": {
                "bucket_name": "blendvision-one-assume-role-source1",
                "external_id": tp['external_id'],
                "path": "blendvisionone",
                "region": "eu-west-1",
                "user_role_arn": tp['role_arn']
            },
            "name": "blendvision-one-cloud-storage",
            "type": "CLOUD_STORAGE_TYPE_AWS"
        } }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# list cloud storages
@cloud_storage_bp.route('/list', methods=['GET'])
def list():
    url = base_url + "/bv/configuration/v1/cloud-storages"
    querystring = {"current_page":"1","items_per_page":"1"}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()