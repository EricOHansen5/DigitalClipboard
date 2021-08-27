import os, datetime, json, subprocess, shutil
from Configs import Configs
from Common import Common, Logger, LogTypeString as lts
from shutil import copyfile
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

class DeviceMaps(object):    
    successful_load = False
    deviceMaps = {}
    
    def __init__(self):
        self.load_data()


    def load_data(self):
        logger = []
        logger.append(("Load DeviceMaps", lts.GEN))
        #Logger.Add("Load DeviceMaps", lts.GEN)
        try:
            # Check if local/network devicemaps exists
            localexists = os.path.isfile(Configs.local_data)
            networkexists = os.path.isfile(Configs.network_data)

            # Create local devicemaps if not exist
            if localexists is False:
                logger.append(("Local DeviceMaps File Created", lts.GEN))
                #Logger.Add("Local DeviceMaps File Created", lts.GEN)
                with open(Configs.local_data, 'w+') as localdata:
                    localdata.write("")
                    Logger.AddList(logger)
                    return True
            # Create network devicemaps if not exist
            if networkexists is False:
                logger.append(("Network DeviceMaps File Created", lts.GEN))
                #Logger.Add("Network DeviceMaps File Created", lts.GEN)
                with open(Configs.network_data, 'w+') as networkdata:
                    networkdata.write("")
                    Logger.AddList(logger)
                    return True

            # Check local/network file sizes
            localdatasize = os.path.getsize(Configs.local_data)
            networkdatasize = os.path.getsize(Configs.network_data)

            # Network devicemaps smaller than local then load from local
            if localdatasize > networkdatasize or localdatasize == networkdatasize:
                if localdatasize == networkdatasize:
                    #Logger.Add("DeviceMap Files Equal Size", lts.GEN)
                    logger.append(("DeviceMap FIles Equal Size", lts.GEN))
                else:
                    #Logger.Add("Local DeviceMaps Larger Than Network Data", lts.ERR)
                    logger.append(("Local DeviceMaps Larger Than Network Data", lts.ERR))

                with open(Configs.local_data, 'r') as localdata:
                    #Logger.Add(localdata, lts.WAR)
                    self.deviceMaps = json.loads(localdata.read())
                    self.successful_load = True

            # Local devicemaps smaller than network then load from network
            elif networkdatasize > localdatasize:
                #Logger.Add("Network DeviceMaps Larger Than Local Data", lts.ERR)
                logger.append(("Network DeviceMaps Larger Than Local Data", lts.ERR))
                with open(Configs.network_data, 'r') as networkdata:
                    self.deviceMaps = json.loads(networkdata.read())
                    self.successful_load = True
                #Logger.Add("Network DeviceMaps Load Complete", lts.GEN)
                logger.append(("Network DeviceMaps Load Complete", lts.GEN))
                Logger.AddList(logger)

            return True
        except FileNotFoundError:
            logger.append(("File Not Found Error - DeviceMaps", lts.ERR))
            Logger.AddList(logger)
            #Logger.Add("File Not Found Error - DeviceMaps", lts.ERR)
            return False
        except Exception:
            #Logger.Add("Unknown Exception - DeviceMaps: " + sys.exc_info()[0], lts.ERR)
            logger.append(("Unknown Exception - DeviceMaps: " + sys.exc_info()[0], lts.ERR))
            Logger.AddList(logger)
            return False


    def write_data(self):
        logger = []
        logger.append(("Write Data", lts.GEN))
        #Logger.Add("Write Data", lts.GEN)
        try:
            logger.append(("Writing Local DeviceMaps", lts.GEN))
            #Logger.Add("Writing Local DeviceMaps", lts.GEN)
            with open(Configs.local_data, 'w') as localdata:
                localdata.write(json.dumps(self.deviceMaps))
            logger.append(("Writing Network DeviceMaps", lts.GEN))
            #Logger.Add("Writing Network DeviceMaps", lts.GEN)
            with open(Configs.network_data, 'w') as networkdata:
                networkdata.write(json.dumps(self.deviceMaps))

            Logger.Add("Checking Hash Values", lts.GEN)
            if Common.CheckHash(Configs.local_data, Configs.network_data) is False:
                logger.append(("Copying Local File", lts.WAR))
                #Logger.Add("Copying Local File", lts.WAR)
                copyfile(Configs.local_data, Configs.network_data)

            Logger.AddList(logger)
            return True
        except FileNotFoundError:
            logger.append(("File Not Found Error", lts.ERR))
            Logger.AddList(logger)
            #Logger.Add("File Not Found Error", lts.ERR)
            return False
        except Exception:
            #Logger.Add("Unknown Exception", lts.ERR)
            #Logger.Add(sys.exc_info()[0], lts.ERR)
            logger.append(("Unknown Exception", lts.ERR))
            logger.append((sys.exc_info()[0], lts.ERR))
            Logger.AddList(logger)
            return False


    def Add_mapping(self, ecn, barcode, name, checkedin):
        if ecn in self.deviceMaps.keys():
            Logger.Add("{0} already exists. Updating.".format(ecn), lts.GEN)
        else:
            Logger.Add("{0} doesn't exists. Creating.".format(ecn), lts.GEN)
        self.deviceMaps[ecn] = self.Create_map(ecn, barcode, name, checkedin)
        self.write_data()


    def Create_map(self, ecn, barcode, name, checkedin):
        objmap = {}
        objmap["Barcode"] = barcode
        objmap["ECN"] = ecn
        objmap["Name"] = name
        objmap["CheckedIn"] = checkedin
        return objmap
