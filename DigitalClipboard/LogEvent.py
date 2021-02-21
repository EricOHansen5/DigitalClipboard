import datetime

class LogEvent(object):
    date_time = datetime.datetime.now()
    username = "[[no_user]]"
    tech = "[[no_tech]]"
    comment = ["[[init comment]]",]
    ecn = -1
    barcode = -1
    status = "[[no_status]]"

    """This class holds the info needed to track assets going in/out of IMB"""
    def __init__(self, date_time, username, tech, comment, ecn, barcode):
        print("LogEvent Created")
        self.date_time = date_time
        self.username = username
        self.tech = tech
        self.comment = comment.append(comment)
        self.ecn = ecn
        self.barcode = barcode
        self.sig_path = "no_path"

    def __init__(self):
        self.sig_path = "no_path"
        print("LogEvent Created Empty")
        

    def Add_DateTime(self, date_time):
        print("DateTime Added")
        self.date_time = date_time


    def Add_Username(self, username):
        print("Username Added")
        self.username = username


    def Add_Tech(self, tech):
        print("Tech Added")
        self.tech = tech


    def Add_Comment(self, comment):
        print("Comment Added")
        self.comment.append(comment)


    def Add_ECN(self, ecn):
        print("ECN Added")
        self.ecn = ecn


    def Add_Barcode(self, barcode):
        print("Barcode Added")
        self.barcode = barcode


    def Add_Status(self, status):
        print("Status Added")
        self.status = status


    def Add_Signature(self, sig_path):
        print("Signature Path Added")
        self.sig_path = sig_path


    def Get_Log(self):
        print("Get_Log Called")
        # refresh datetime
        if(self.barcode == "-1"):
            return ""

        return "{0}\t{1}\t{2}\t[[{3}]]\t[[{4}]]\t[[{5}]][[{6}]]\n".format(f'{self.date_time:%Y-%m-%d_%H:%M.%S}', self.status, self.barcode, self.ecn, self.username, self.tech, self.sig_path)

