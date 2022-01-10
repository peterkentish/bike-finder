from os import stat
from data_fetcher import *
import urllib.parse
import logging

GOOGLE_API_KEY = "AIzaSyDYiFGHvMa1Kx_nH2P3e5w_47EDhnjxg6A"
GOOGLE_GEOCODE_API_PATH = "https://maps.googleapis.com/maps/api/geocode/json?"



def get_lat_lon(address):

    full_url = add_key(GOOGLE_GEOCODE_API_PATH+stringify_address_data(address))
    data = basic_fetch(full_url, None)
    location_data = data["results"]
    if (len(location_data) > 1):
        return "location too ambigious"

    first_result = location_data[0]["geometry"]["location"]
    lat = first_result["lat"]
    long = first_result["lng"]
    return (lat, long)

def url_encode_string(string_to_encode):
    return urllib.parse.quote_plus(string_to_encode)

def add_key(url):
    return url + "&key="+GOOGLE_API_KEY

def stringify_address_data(address_data):
    stateOrRegion = address_data["stateOrRegion"]
    city = address_data["city"]
    countryCode  = address_data["countryCode"]
    postalCode  = address_data["postalCode"]
    addressLine1  = address_data["addressLine1"]
    addressLine2  = address_data["addressLine2"]
    addressLine3  = address_data["addressLine3"]
    districtOrCounty = address_data["districtOrCounty"]
    address_as_list = [addressLine1, addressLine2, addressLine3, city, stateOrRegion, postalCode, districtOrCounty, countryCode]
    address_as_query = ""
    for i in address_as_list:
        if (i !="" and i is not None):
            address_as_query += (i +", ")
    
    return "address=" + remove_suffix(address_as_query, ", ")

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def get_alexa_device_location(system_context):
    device_id = system_context.device.device_id
    api_access_token = system_context.api_access_token
    api_endpoint = system_context.api_endpoint

    request_path = ("/v1/devices/{deviceId}/settings/address").format(deviceId = device_id)

    headers = {
         'Authorization': 'Bearer ' + api_access_token,
         'Accept': 'application/json'
    }
    full_request = api_endpoint + request_path

    #will return 403 forbidden if address has not been allowed
    address_data = basic_fetch(full_request, headers)
    
    return address_data

