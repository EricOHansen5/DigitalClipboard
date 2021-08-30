import os.path, hashlib
from Configs import Configs
from os import path
from Common import Common
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import datetime

class Datastore(object):
    """Class for adding Digital Clipboard log entries"""
    isuselocal = False

    def __get_date(self):
        # Get the date for this weeks monday (start of week)
        Configs.monday_date = datetime.datetime.today()  - datetime.timedelta(days=datetime.datetime.today().weekday() % 7)


    def __set_readonly(self):
        print("Set_Readonly")
        # Set readonly permissions
        os.chmod(Configs.localfilename, S_IREAD|S_IRGRP|S_IROTH)
        os.chmod(Configs.filename, S_IREAD|S_IRGRP|S_IROTH)


    def __set_writable(self):
        print("Set_Writable")
        # Set readonly permissions
        os.chmod(Configs.localfilename, S_IWUSR|S_IREAD)
        os.chmod(Configs.filename, S_IWUSR|S_IREAD)


    def __check_file(self):
        print("Check_File")
        # Check to see if a log file exists already
        log_exists = path.exists(Configs.filename)
        log_dir_exists = path.exists(Configs.checkpath)
        local_exists = path.exists(Configs.localfilename)
        local_dir_exists = path.exists(Configs.localpath)

        # check and create directories as needed
        if log_dir_exists is False:
            os.mkdir(Configs.checkpath)
        log_dir_exists = path.exists(Configs.checkpath)

        if local_dir_exists is False:
            os.mkdir(Configs.localpath)
        local_dir_exists = path.exists(Configs.localpath)

        # check and create files as needed
        if log_dir_exists and local_dir_exists:
            if local_exists is False:
                log_file = open(Configs.localfilename, "w+")
                log_file.close()
            if log_exists is False:
                log_file = open(Configs.filename, "w+")
                log_file.close()
            self.__set_readonly()


    def __init__(self):
        print("Datastore Created")

        # Get the first day of the week in this case 'MONDAY'
        self.__get_date()
        
        # Create file if it doesn't exist
        self.__check_file()
        

    def __add_log_entry(self, log_entry):
        print("Add_Log_Entry")

        # Change permission to writable
        self.__set_writable()

        # Append to log file
        log_file1 = open(Configs.localfilename, "a+")
        log_file2 = open(Configs.filename, "a+")

        # Write line to file
        log_file1.write(log_entry)
        log_file2.write(log_entry)

        # Close log file
        log_file1.close()
        log_file2.close()

        # Change permission to read-only
        self.__set_readonly()
        
        # Check hash for local and network copy
        self.__get_hash()


    def __get_hash(self):
        return Common.CheckHash(Configs.localfilename, Configs.filename)


    # Append the given log entry line to the current local/remote log files.
    def Add(self, log_entry):
        print("Datastore Add Called")
        # Check day of the week depending on how long program has been running
        self.__get_date()

        # Check to see if a log file exists already
        self.__check_file()

        # Add log entry
        self.__add_log_entry(log_entry)

        print("Datastore Add Complete")


