import os.path
from os import path
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import datetime
import json


class DeviceMaps(object):    

    # Share Drive
    jsonPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\Database.json";
    jsonDir  = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\";

    def __init__(self):
        print("DeviceMaps Created")

        # load data from file
        data = open(self.jsonPath,)

        # deserialize data
        self.jsonMap = json.load(data)
        
        print("DeviceMaps Complete")

        