from DeviceMaps import DeviceMaps
from Configs import Configs
from Logger import Logger
from LogTypeString import LogTypeString as lts

def test_load_data():
    if DeviceMaps().load_data():
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)

def test_load_data_local_larger():
    #TODO -----------------------------------------
    Logger.Add("FAILED", lts.ERR)


def test_load_data_local_smaller():
    #TODO -----------------------------------------
    Logger.Add("FAILED", lts.ERR)


def test_load_data_files_equal():
    #TODO -----------------------------------------
    Logger.Add("FAILED", lts.ERR)


def test_write_data():
    if DeviceMaps().write_data():
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)

def test_Create_map():
    ecn = "9999"
    barcode = "90909"
    name = "test_map"
    checkedin = True
    dm = DeviceMaps()
    obj = dm.Create_map(ecn, barcode, name, checkedin)

    if obj["Barcode"] == "90909" and obj["ECN"] == "9999" and obj["Name"] == "test_map" and obj["CheckedIn"] == True:
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)


def test_Add_mapping():
    dm = DeviceMaps()
    size1 = len(dm.deviceMaps.keys())
    dm.Add_mapping("8888", "barcode123", "test_add_mapping name", True)
    size2 = len(dm.deviceMaps.keys())
    if size1 < size2:
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)


# Run Tests
# LOAD DATA #
test_load_data()
test_load_data_local_larger()
test_load_data_local_smaller()
test_load_data_files_equal()

# WRITE DATA #
test_write_data()

# CREATE MAPS #
test_Create_map()

# ADD MAPPING #
test_Add_mapping()
