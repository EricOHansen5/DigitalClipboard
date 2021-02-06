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

    def __init__(self):
        print("LogEvent Created Empty")
        


    def Add_Username(self, username):
        print("Username Added")
        self.username = "[[{0}]]".format(username)


    def Add_Tech(self, tech):
        print("Tech Added")
        self.tech = "[[{0}]]".format(tech)


    def Add_Comment(self, comment):
        print("Comment Added")
        self.comment.append(comment)


    def Add_ECN(self, ecn):
        print("ECN Added")
        self.ecn = "[[{0}]]".format(ecn)


    def Add_Barcode(self, barcode):
        print("Barcode Added")
        self.barcode = barcode


    def Add_Status(self, status):
        print("Status Added")
        self.status = status


    def Get_Log(self):
        print("Get_Log Called")
        # refresh datetime
        if(self.barcode == "-1"):
            return ""

        self.date_time = datetime.datetime.now()
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(f'{self.date_time:%Y-%m-%d_%H:%M.%S}', self.status, self.barcode, self.ecn, self.username, self.tech)


