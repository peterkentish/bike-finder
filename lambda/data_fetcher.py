from os import close
import requests
import logging
import json
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

STATION_INFORMATION = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
STATION_STATUS = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status"


def fetch_stations(url):
     # construct systems api timezone url
    try:
        r = requests.get(url)
        res = r.json()
        return res["data"]["stations"]
    except Exception:
        logger.error("Failed to retrieve data for " + url)
        return 501


def basic_fetch(url, headers):
    try:
        r = requests.get(url, headers=headers)
        if (r.status_code == requests.codes.forbidden):
            return 403
        res = r.json()
        return res
    except Exception:
        logger.error("Failed to retrieve data for " + url)

def send_directive(speech, request_data):
    system_context = request_data.context.system
    api_access_token = system_context.api_access_token
    api_endpoint = system_context.api_endpoint
    request_id = request_data.request.request_id

    full_endpoint_url = api_endpoint+ "/v1/directives"
    
    headers = {
        'Authorization': 'Bearer ' + api_access_token,
        'Content-Type': 'application/json'
    }
    data = { 
        "header":{ 
            "requestId": request_id
        },
        "directive":{ 
            "type":"VoicePlayer.Speak",
            "speech":"<speak>" + speech + "</speak>"
    }
    }
    try:
        r = requests.post(full_endpoint_url,data=json.dumps(data), headers=headers)
        logger.info(r.status_code)
    except Exception:
        logger.error("Failed to retrieve data for " + full_endpoint_url)



