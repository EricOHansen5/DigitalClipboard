import os.path, datetime, json, subprocess
from os import path
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

class DeviceMaps(object):    

    # Share Drive
    jsonPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\Database.json";
    BAKjsonPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\Database.jsonBAK";
    jsonDir  = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\";
    dcOnlyJsonPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\DC_Only_Database.json";

    successful_load = False

    def __init__(self):
        print("DeviceMaps Created")
        
        # flag to choose default json db or backup db
        self.successful_load = True

        # loop through until data is loaded from default json db or backup db
        while True:
            try:
                if self.successful_load:
                    filename = self.jsonPath
                    print("Default json DB")
                else:
                    filename = self.BAKjsonPath
                    print("Backup json DB")

                # load data from file
                with open(filename, 'r') as jfile:
                    data = jfile.read()

                # deserialize data
                self.jsonMap = json.loads(data)
                break
            except:
                if not self.successful_load:
                    print("Unable to load either json db's")
                    break
                print("problem with loading json db")
                self.successful_load = False

        if not self.load_dc_only_maps():
            self.write_dc_only_maps()

        print("DeviceMaps Complete")


    def load_dc_only_maps(self):
        try:
            # init data to be filled
            data = ""
            with open(self.dcOnlyJsonPath, 'r') as jdata:
                data = jdata.read() # fill data with json data

            self.dcJsonMaps = json.loads(data)
            print("DC only loaded successfully")
            return True
        except:
            print("DC only unable to load")
            return False


    def write_dc_only_maps(self):
        try:
            if not hasattr(self, "dcJsonMaps"):
                self.dcJsonMaps = {}

            jobj = json.dumps(self.dcJsonMaps)

            # Before
            filesize1 = os.path.getsize(self.dcOnlyJsonPath)

            # write local copy
            with open("DC_Only_Database.json", 'w+') as ofile:
                ofile.write(jobj)

            # write network location
            with open(self.dcOnlyJsonPath, 'w+') as ofile:
                ofile.write(jobj)

            # After
            filesize2 = os.path.getsize(self.dcOnlyJsonPath)
            if filesize2 < filesize1:
                print("DC_Only - File size is smaller then before.")
            elif filesize2 == filesize1:
                print("DC_Only - File size is equal.")
            else:
                print("DC_Only - File size is larger then before.")


            print("Created dc only maps json db successful")
        except:
            print("Unable to create dc only maps json db")


    def Add_mapping(self, ecn, barcode, name):
        exist = False

        for k in self.jsonMap['Mappings']:
            if self.jsonMap['Mappings'][k]['Barcode'] == barcode:
                exist = True

        if not exist:
            print("{0} doesn't exists. Creating.")
            if len(self.dcJsonMaps) >= 0:
                self.Create_map(ecn, barcode, name)
                self.dcJsonMaps[ecn] = self.objmap
            self.write_dc_only_maps()
            subprocess.Popen('\\\\riemfs01\\x\\AutomationTools\\Digital_Clipboard_Admin\\Executable\\DigitalClipboardSync.exe')

        else:
            print("{0} already exists. Updating.")


    def Create_map(self, ecn, barcode, name):
        self.objmap = {}
        self.objmap["Barcode"] = barcode
        self.objmap["DeviceModelID"] = ''
        self.objmap["ECN"] = ecn
        self.objmap["Name"] = name
