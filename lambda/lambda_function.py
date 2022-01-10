# -*- coding: utf-8 -*-
import logging
import ask_sdk_core.utils as ask_utils
import os

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from data_fetcher import *
from aws_defaults import *
from distance_calculator import *
from location import *
from bicing_data_utils import *
from language_utils import Language
from ask_sdk_model import Response
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for first time Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        alexa_request_data = handler_input.request_envelope
        locale = ask_utils.request_util.get_locale(handler_input)
        language = Language(locale)
        send_directive(language.get_response('first.intro'), alexa_request_data)

        attributes_manager = handler_input.attributes_manager

        # TODO Put all these calls into location.py
        device_location = get_alexa_device_location(handler_input.request_envelope.context.system)
        if (device_location == 403):
            return (
            handler_input.response_builder
                 .speak(language.get_response('intro.permission.denied'))
                .response
        )

        (lat, long) = get_lat_lon(device_location)
       
        station_information_data = fetch_stations(STATION_INFORMATION)
        if (station_information_data == 501):
            return (
            handler_input.response_builder
                .speak(language.get_response('bicing.api.failure'))
                .response
        )

        closest_stations = get_five_closest_stations(station_information_data, lat, long)
        user_data = {
            "first_station": closest_stations[0],
            "second_station":  closest_stations[1],
            "third_station":  closest_stations[2],
            "fourth_station":  closest_stations[3],
            "fifth_station":  closest_stations[4],
            "first_time": "True",
        }
    
        attributes_manager.persistent_attributes = user_data
        attributes_manager.save_persistent_attributes()
        


        speak_output = language.get_response('intro.success')

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class HasFavouriteStationConfiguredRequestHandler(AbstractRequestHandler):
    """Handler for skill launch after favourite station is set"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
         # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("first_station" in attr)

        return attributes_are_present and ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):

        locale = ask_utils.request_util.get_locale(handler_input)
        language = Language(locale)
        send_directive(language.get_response('checking.directive'), handler_input.request_envelope)
        # TODO remove data manipulation logic from here

        attr = handler_input.attributes_manager.persistent_attributes
        first_station_id = int(attr["first_station"])
        second_station_id = int(attr["second_station"])
        third_station_id = int(attr["third_station"])
        is_first_time = attr["first_time"]
        station_status = fetch_stations(STATION_STATUS)


        speak_output = get_speech_output_for_stations(language, station_status, first_station_id, second_station_id, third_station_id)
        
        if (is_first_time == "True"):
            speak_output += language.get_response('first.tutorial')
            handler_input.attributes_manager.persistent_attributes["first_time"] = "False"
            handler_input.attributes_manager.save_persistent_attributes()

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
class ResetAccountRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ResetAccountIntent")(handler_input)
    
    def handle(self, handler_input):
        attributes_manager = handler_input.attributes_manager
        attributes_manager.delete_persistent_attributes()
        locale = ask_utils.request_util.get_locale(handler_input)
        language = Language(locale)

        return (
            handler_input.response_builder
                .speak(language.get_response('account.reset'))
                .response
        )

        

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)
sb.add_request_handler(HasFavouriteStationConfiguredRequestHandler())
sb.add_request_handler(LaunchRequestHandler()) 
sb.add_request_handler(ResetAccountRequestHandler()) 
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())
lambda_handler = sb.lambda_handler()