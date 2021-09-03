import os.path, datetime

class Configs(object):
    """Mostly paths used by the Digital Clipboard program"""
    dictConfigs = {}
    baseUri = '\\\\riemfs01\\X\\AutomationTools\\'
    dc_logs = 'Digital_Clipboard_Logs\\'
    dc_admin = 'Digital_Clipboard_Admin\\'
    logfile = os.path.join(baseUri, "pypi/DigitalClipboard/logs.txt")

    ##----- DATASTORE -----##
    monday_date = datetime.datetime.today()  - datetime.timedelta(days=datetime.datetime.today().weekday() % 7)
    date_format = f'{monday_date:%Y-%m-%d}.log'

    # Share Drive
    dirpath = baseUri + dc_logs
    sigpath = baseUri + dc_logs + "Signatures\\"
    checkpath = "\\\\riemfs01\\X\\"
    filename = os.path.join(dirpath, date_format)
    
    # Local Drive
    desktoppath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    localpath = os.path.join(desktoppath, "DC_Logs")
    localfilename = os.path.join(localpath, date_format)
    ##----- END -----##


    ##----- DEVICEMAPS ------##
    # Share Drive [DEPRECATED]
    jsonPath = baseUri + dc_admin + "Database.json";
    BAKjsonPath = baseUri + dc_admin + "Database.jsonBAK";
    jsonDir  = baseUri + dc_admin
    dcOnlyJsonPath = baseUri + dc_admin + "DC_Only_Database.json";
    dcSyncPath = baseUri + dc_admin + 'Executable\\DigitalClipboardSync.exe'
    
    # USED FOR ALL DEVICE TO BARCODE MAPPINGS
    local_data = os.path.join(desktoppath, "Data.json")
    network_data = baseUri + dc_admin + "Data.json"
    ##----- END ------##

    def UpdateConfigs(self):
        # TODO add all filepaths to dictionary
        print("Update Configs")


    def WriteConfigs(self):
        # TODO write dictionary to configs file
        print("Write Configs")


    dcConfigsPath = baseUri + dc_admin + "Configs.json";
    def ReadConfigs(self):
        # TODO read dictionary from config file
        print("Read Configs")

