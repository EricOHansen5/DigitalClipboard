import hashlib, os, datetime, json
from Configs import Configs
from enum import Enum

class LogTypeString(Enum):
    GEN = "-- GENERAL  --"
    WAR = "-- WARNING  --"
    ERR = "-- ERROR    --"
    CRIT ="-- CRITICAL --"

class Common:
    def CheckHash(file1, file2):
        file1hash = ""
        file2hash = ""

        # Check File Size
        s1 = os.path.getsize(file1)
        s2 = os.path.getsize(file2)
        if s2 > s1:
            print(file2, "Larger than", file1)
            return False
        elif s1 > s2:
            print(file1, "Larger than", file2)
            return False
        else:
            print("Files are the same size")

        # Check Hashs
        with open(file1, 'rb') as filedata1:
            file1hash = hashlib.md5(filedata1.read()).hexdigest()

        with open(file2, 'rb') as filedata2:
            file2hash = hashlib.md5(filedata2.read()).hexdigest()

        if file1hash == file2hash:
            Logger.Add("{0} : {1} --- {2}".format(file1hash, file2hash, "MD5 Verified."), LogTypeString.GEN)
            return True
        else:
            Logger.Add("{0} : {1} --- {2}".format(file1hash, file2hash, "MD5 Verification FAILED."), LogTypeString.ERR)
            return False


class Logger:
    def Add(msg, type):
        dt = datetime.datetime.now()
        spacing = "\n"
        if "----" in str(msg):
            spacing = spacing * 3
        entry = "{0}\t{1}\t{2}".format(dt, type.value, msg)
        entry = spacing + entry
        print(entry)
        if os.path.isfile(Configs.logfile):
            with open(Configs.logfile, "a") as logfile:
                logfile.write(entry)
        else:
            print("Logger File Created")
            with open(Configs.logfile, "w") as logfile:
                logfile.write(entry)

