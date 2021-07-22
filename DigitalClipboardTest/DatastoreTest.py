from Datastore import Datastore
from Configs import Configs
from Logger import Logger
from LogTypeString import LogTypeString as lts

def test_Add_Pass():
    testentry = "some test entry"
    Datastore().Add(testentry)
    
    stringdata = ""    
    with open(Configs.localfilename, 'r') as logfile:
        stringdata = logfile.read()

    if testentry in stringdata:
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)

# Run Tests
test_Add_Pass()
