from os import stat
from location import stringify_address_data
from location import url_encode_string
from location import add_key
from location import GOOGLE_API_KEY
from location import get_lat_lon
from location import get_alexa_device_location
from bicing_data_utils import get_station_status_from_id
from bicing_data_utils import response_logic
from data_fetcher import fetch_stations
from data_fetcher import STATION_STATUS
import unittest
from sample_data import SAMPLE_REQUEST
from language_utils import Language
class TestSum(unittest.TestCase):
    test_address = {
            "stateOrRegion" : "WA",
            "city" : "Seattle",
            "countryCode" : "US",
            "postalCode" : "98109",
            "addressLine1" : "410 Terry Ave North",
            "addressLine2" : "",
            "addressLine3" : "aeiou",
            "districtOrCounty" : ""
            }
    language = Language('en-GB')
    


    def test_stringify_address(self):
        test_address_as_string = stringify_address_data(self.test_address)
        expected_address = "address=410 Terry Ave North, aeiou, Seattle, WA, 98109, US" 
        self.assertEqual(test_address_as_string, expected_address, "Test address was not stringified correctly")

    def test_url_encode_address(self):
        actual_result = url_encode_string("410 Terry Ave North, aeiou, Seattle, WA, 98109, US" )
        expected_result= "410+Terry+Ave+North%2C+aeiou%2C+Seattle%2C+WA%2C+98109%2C+US"
        self.assertEqual(actual_result, expected_result, "Test address was not encoded correctly")
    
    def test_add_google_api_key(self):
        test_string = "some.url.string"
        actual_result = add_key(test_string)
        expected_result = "some.url.string&key="+GOOGLE_API_KEY
        self.assertEqual(actual_result, expected_result, "The key was not appeneded to the URL correctly")
    
    def test_no_bikes(self):
        expected_result = self.language.get_response('main.nobikes')
        actual_result = response_logic(self.language, 0,0,0,0,0,0)
        self.assertEqual(actual_result, expected_result, "The no bikes message was not correctly sent")

    def test_closest_station_both_types(self):
        mech = 5
        elec = 5
        expected_result = self.language.get_response('main.closest.both.types').format(mech, elec)
        actual_result = response_logic(self.language, mech,elec,0,0,0,0)
        self.assertEqual(actual_result, expected_result, "The closest station both types message was not correct")
    
    def test_mechanical_at_first_one_electrical_at_second(self):
        mech = 5
        elec = 1
        expected_result = self.language.get_response('main.some.mechanical.no.electrical').format(mech) + self.language.get_response('main.closest.ebike.at.second.solo')
        actual_result = response_logic(self.language, mech,0,0,elec,0,0)
        self.assertEqual(actual_result, expected_result, "some mechanical and one electrical at second station was not correct")

    def test_mechanical_at_first_multiple_electrical_at_second(self):
        mech = 5
        elec = 5
        expected_result = self.language.get_response('main.some.mechanical.no.electrical').format(mech) + self.language.get_response('main.closest.ebike.at.second.multiple').format(elec)
        actual_result = response_logic(self.language, mech,0,0,elec,0,0)
        self.assertEqual(actual_result, expected_result, "some mechanical at first and multiple electrical at second station was not correct")

    def test_mechanical_at_first_one_electrical_at_third(self):
        mech = 5
        elec = 1
        expected_result = self.language.get_response('main.some.mechanical.no.electrical').format(mech) + self.language.get_response('main.closest.ebike.at.third.solo')
        actual_result = response_logic(self.language, mech,0,0,0,0,elec)
        self.assertEqual(actual_result, expected_result, "some mechanical at first and single electrical at third station was not correct")

    def test_mechanical_at_first_multiple_electrical_at_third(self):
        mech = 5
        elec = 3
        expected_result = self.language.get_response('main.some.mechanical.no.electrical').format(mech) + self.language.get_response('main.closest.ebike.at.third.multiple').format(elec)
        actual_result = response_logic(self.language, mech,0,0,0,0,elec)
        self.assertEqual(actual_result, expected_result, "some mechanical at first and multiple electrical at third station was not correct")

    def test_no_mechanical_at_first_multiple_electrical_at_third(self):
        mech = 5
        elec = 3
        expected_result = self.language.get_response('main.some.mechanical.no.electrical').format(mech) + self.language.get_response('main.closest.ebike.at.third.multiple').format(elec)
        actual_result = response_logic(self.language, mech,0,0,0,0,elec)
        self.assertEqual(actual_result, expected_result, "some mechanical at first and multiple electrical at third station was not correct")
    def test_nothing_at_first_just_mechanical_at_second(self):
        mech = 5
        expected_result = self.language.get_response('main.first.station.empty') \
            + self.language.get_response('main.closest.ebike.not.available') \
            + self.language.get_response('main.closest.mbike.at.second.multiple').format(mech)
        actual_result = response_logic(self.language, 0,0,mech,0,0,0)
        self.assertEqual(actual_result, expected_result, "some mechanical at first and multiple electrical at third station was not correct")

    def test_nothing_at_first_just_electrical_at_second(self):
        elec = 5
        expected_result = self.language.get_response('main.first.station.empty') \
            + self.language.get_response('main.closest.ebike.at.second.multiple').format(elec) \
            + self.language.get_response('main.closest.mbike.not.available') 
        actual_result = response_logic(self.language, 0,0,0,elec,0,0)
        self.assertEqual(actual_result, expected_result, "some mechanical at first and multiple electrical at third station was not correct")
    def test_nothing_at_first_just_electrical_at_second(self):
        elec = 5
        mech = 4
        expected_result = self.language.get_response('main.first.station.empty') \
            + self.language.get_response('main.closest.ebike.at.second.multiple').format(elec) \
            + self.language.get_response('main.closest.mbike.at.second.multiple').format(mech) 
        actual_result = response_logic(self.language, 0,0,mech,elec,0,0)
        self.assertEqual(actual_result, expected_result, "some mechanical at first and multiple electrical at third station was not correct")
    






if __name__ == '__main__':
    unittest.main()