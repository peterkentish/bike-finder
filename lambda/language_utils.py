
import yaml
import os
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
class Language:

    def __init__(self, locale):
        self.locale = locale
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        try:
            file_path = './languages/{locale}.yaml'.format(locale=self.locale)
            with open(file_path) as file:
                self.localised_strings = yaml.load(file, Loader=yaml.FullLoader)
        except:
            generic_language = locale[0:2]
            logger.info("Failed to open specific locale file, checking for generic language: " + generic_language)
            if (generic_language == 'es'):
                file_path = './languages/{locale}.yaml'.format(locale='es-ES')
                with open(file_path) as file:
                    self.localised_strings = yaml.load(file, Loader=yaml.FullLoader)
            else:
                logger.info("defaulting to en-GB")
                file_path = './languages/en-GB.yaml'
                with open(file_path) as file:
                    self.localised_strings = yaml.load(file, Loader=yaml.FullLoader)
    
    def get_response(self, translation_code):        
            return self.localised_strings[translation_code]
