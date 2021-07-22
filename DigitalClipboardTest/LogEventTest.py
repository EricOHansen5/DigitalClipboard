from LogEvent import LogEvent
from Configs import Configs
from Logger import Logger
from LogTypeString import LogTypeString as lts
import datetime

def test_Get_Log_Pass():
    event = LogEvent()
    
    event.Add_Barcode("testbarcode")
    event.Add_Comment("test comment")
    event.Add_DateTime(datetime.datetime.now())
    event.Add_Status("--IN --")
    event.Add_ECN("9999")
    event.Add_Signature("test_sig.png")
    event.Add_Username("test user")

    if event.Get_Log() == "{0}\t{1}\t{2}\t[[{3}]]\t[[{4}]]\t[[{5}]]\t[[{6}]]\t[[{7}]]\n".format(f'{event.date_time:%Y-%m-%d_%H:%M.%S}', event.status, event.barcode, event.ecn, event.username, event.tech, event.comment, event.sig_path):
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)

# Run Tests
test_Get_Log_Pass()



