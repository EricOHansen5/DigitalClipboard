import os, datetime
from Configs import Configs
from LogTypeString import LogTypeString

class Logger:
    def Add(msg, type):
        dt = datetime.datetime.now()
        entry = "\n{0}\t{1}\t{2}".format(dt, type.value, msg)
        print(entry)
        with open("logs.txt", "a+") as logfile:
            logfile.write(entry)

