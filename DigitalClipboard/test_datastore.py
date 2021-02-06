import unittest
from DigitalClipboard import Datastore as ds
import datetime as dt

class Test_datastore(unittest.TestCase):
    
    # Test Get_Date
    def test_get_date(self):
        mon = dt.datetime.today() - dt.timedelta(days=dt.datetime.today() % 7)
        print("Date:",mon,sep=' ')
        ds_date = Datastore.get_date()
        self.assertEqual(mon, ds_date, msg="Date Match")

if __name__ == '__main__':
    unittest.main()
