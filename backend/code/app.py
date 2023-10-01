from flask import Flask, jsonify, request
import http.client
import requests

app = Flask(__name__)

base_url = "https://api.one-stage.kkstream.io"
# api_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE3N2RhODVjLTllZjgtNTVjYS05M2FkLTAyYTMyZjkwZjg2MyIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcmJpdCIsInN1YiI6IjZiYTZhMWEzLWM2NjQtNGRmNC04N2ExLWY3NWJmZGY5MmU3NSIsImp0aSI6IjQ2Y2ViMjAyLTg4MDItNDQ4ZC05Mjg5LTc5MjEwOGRmN2U0NiIsInRva2VuX3VzZSI6ImFwaV9hY2Nlc3MiLCJlbWFpbCI6InJpY2hhcmQxMjAzMTBAZ21haWwuY29tIn0.S3Hek-V8DrdnaKWMZE19CFFmflmBBjmIcMuz8a17rb-MR0oyiRdsCyiU1lG3ueDz2PHtGT87lTIwfj7nnk2LkHypMdNXWywdf7bpcylFhVbG0dnbuPsQwpoqZcfDar-j-G5vNZookKnf-elLyHbr6g72LF-Spi6n2Zl41xeyR8LttaEYCmvQw8PTaTC2zXNX0Ev1BwGKwS699Ofup7B8ua7n38HquvRkaB8yZKJTowmSN1CeVfxh3IU1T7LInNlMdHda6X8OaEnZiZ6S3-Z4Kfbig6IVxzwgpSX7zpa79Ekl6LrYYeNlE_va7mR7QPF7pxwWB1F5TSVncp2GQSNRx-DR3GnU7ehQZZPVmmwnXqI4xdegHrj_nJV__Q9YkAF1Vep_kpEXRSb8HkF6bgwnV0rjnpLqqg5gAF2QBa5z0Rcfr-lXOqmmVz_X2Md3VR0IcZ5dp4tXyiO06x05oaE4G3HpRftMC-KGmmiNZNkNKTdtzduPzujJdipDvh5saoKc4dtGCTmR6EeWQa6XRoeBCPV-FxH36O2Gf6VFmZQDlIAPKq2jeAZuszHZwQ9EkOFDH6p_8KdEJXzm_fFVoGCfKId9_KE8NMc6qT8xKTwUEerMK4Er_lzkP1iQQcCLIRRMtKK8ppa5cHCDsIFzdqvuTloY0Xochm3JTGz1fyykqHY"
api_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE3N2RhODVjLTllZjgtNTVjYS05M2FkLTAyYTMyZjkwZjg2MyIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcmJpdCIsInN1YiI6ImMyMmRjZTE3LWQ2M2QtNDY0ZC05NTUzLTQ5YjcwNWQ1YzA1NyIsImp0aSI6ImNiNjY5OGM5LWI4MGItNDI3Yi04YWUwLTJmYTJhOGJhYzI5MSIsInRva2VuX3VzZSI6ImFwaV9hY2Nlc3MiLCJlbWFpbCI6IkhhbmsudHUuY2hAZ21haWwuY29tIn0.p7wDXcJYbKRDcQVNcfphr41d02YVpUjQKuBpdfIMLGYKKcADaCQeb5ib2Gy3NTpm4C4IhTOHrxgx_aB6SmQrYALwZfMrXcyKSd6I9o6gjk7oSReshrQbmlP6Ws5fAWFycXVihcvy2TRb6gHfJ9yz8mq_zrFB416ZPoQUUgctrXJVfJTUxvR4zfYvW2cnutJRMljLWf3xO3PkHBN2Wd0yD7AMPj9DQCyANdNyXoahKpbZRNWykfKJZzREYIfe3AwqpF6n_MgwT3vFwnDXQT3zI138QI821NdxLTMvkX2R6AhqQ0LbUPP80KcqjJr9unhNkpYRJPkjkKm4fskAFcQJm1D0eSiwg2Zotgr_9wgpXTKSUjp-yC9Rvpp6CqIIect9umOZIQYxjquH0Pvrqj9MdbG4EfgPx4HxHePQ8MyFhSCg-aJF0LA6gFHakywKi3NOcTAhaBtyC0jyoziiBwRZyOWthDkcjDIzJsINOYLgzI492v9Pf1VCJBZNb7qQ3Fgqcc9hh5GpRTt35fzGAnIWA4vuoYR4uBq76MqJbmwBQf_KObDVILuHtji9hxMfqfATg_WDDOwUSuBvFhct6k2PQ6hzZjaWdNmG9fvJhrBXdKxpx1pliD3am6Hab-uv58zYknUf10L-UHK6C-y9CK_-epMhSYdk20P0hdNAVK9wQBg"
org_id = "83f4d633-368a-4163-bbc8-359c7ff56559"


@app.route('/welcome', methods=['GET'])
def welcome():
    return "hello, world"

# @app.route('/list_account', methods=['GET'])
# def list_account():
#     return

# list every files under your current account
@app.route('/file_list', methods=['GET'])
def list_files():
    url = base_url + "/bv/cms/v1/library/files"
    querystring = {"current_page":"1","items_per_page":"1","type":"FILE_TYPE_UNSPECIFIED"}
    headers = {
    "x-bv-org-id": org_id,
    "Accept": "application/json",
    "authorization": "Bearer " + api_token
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# creat VOD
@app.route('/vod_create', methods=['POST'])
def vod_create():
    url = base_url + "/bv/cms/v1/vods"

    payload = {
        "metadata": {
            "long_description": "",
            "short_description": ""
        },
        "name": "IMG_1882.MOV",
        "profile_set_id": "6a2b2ea3-9e35-4216-93c9-da09dee5ab12",
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
                "subtitles": [
                    {
                        "code": "eng",
                        "display": "English",
                        "id": "ff59095c-fd67-4edc-9705-5e56c31b3577",
                        "name": "english.vtt"
                    }
                ],
                "video": { "id": "c6f50caa-37ab-4d8c-9b06-e231544d598f" }
            },
            "type": "SOURCE_TYPE_LIBRARY"
        }
    }
    headers = {
        "x-bv-org-id": org_id,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "authorization": "Bearer " + api_token
    }

    response = requests.post(url, json=payload, headers=headers)

    # print(response.json())
    return response.json()

@app.route('/file_upload', methods=['POST'])
def file_upload():

    url = base_url + "/bv/cms/v1/library/files:upload"

    payload = { "file": {
            "name": request.values['name'],
            "size": request.values['size'],
            "source": request.values['source'],
            "type": request.values['type']
        } }
    headers = {
        "x-bv-org-id": org_id,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "authorization": "Bearer " + api_token
    }

    response = requests.post(url, json=payload, headers=headers)

    # print(response.json())
    return response.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port='5000')