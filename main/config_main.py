import os
import json
import traceback
import logging

def read_config_json(name_config):
    try:
        #PATH_SCRIPT = os.path.abspath(__file__)
        PATH_SCRIPT_DIR = os.path.abspath(os.curdir)
        PATH_CONFIG_DIR = PATH_SCRIPT_DIR + '/main/configs'

        with open(PATH_CONFIG_DIR + '/' + name_config) as config:
            return json.loads(config.read())
    except Exception as e:
        logging.error(traceback.format_exc())
        return str(e)