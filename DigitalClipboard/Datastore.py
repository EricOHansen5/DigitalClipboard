import os.path
from Configs import Configs
from os import path
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import datetime

class Datastore(object):
    """description of class"""
    isuselocal = False

    def __get_date(self):
        # Get the date for this weeks monday (start of week)
        Configs.monday_date = datetime.datetime.today()  - datetime.timedelta(days=datetime.datetime.today().weekday() % 7)


    def __set_readonly(self):
        print("Set_Readonly")
        if self.isuselocal:
            os.chmod(Configs.localfilename, S_IREAD|S_IRGRP|S_IROTH)
        else:
            # Set readonly permissions
            os.chmod(Configs.filename, S_IREAD|S_IRGRP|S_IROTH)


    def __set_writable(self):
        print("Set_Writable")
        if self.isuselocal:
            os.chmod(Configs.localfilename, S_IWUSR|S_IREAD)
        else:
            # Set readonly permissions
            os.chmod(Configs.filename, S_IWUSR|S_IREAD)


    def __check_file(self):
        print("Check_File")
        # Check to see if a log file exists already
        log_exists = path.exists(Configs.filename)
        local_exists = path.exists(Configs.localfilename)
        local_dir_exists = path.exists(Configs.localpath)

        if path.exists(Configs.checkpath):
            self.isuselocal = False
            # If file doesn't exist create it
            if log_exists is False:
                log_file = open(Configs.filename, "w+")
                log_file.close()

                # Change permissions on file to read-only
                self.__set_readonly()
        else:
            self.isuselocal = True
            if local_exists is False:
                if local_dir_exists is False:
                    os.mkdir(Configs.localpath)
                log_file = open(Configs.localfilename, "w+")
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

        if self.isuselocal:
            log_file = open(Configs.localfilename, "a+")
        else:
            # Append to log file
            log_file = open(Configs.filename, "a+")
        
        # Write line to file
        log_file.write(log_entry)

        # Close log file
        log_file.close()

        # Change permission to read-only
        self.__set_readonly()


    def Add(self, log_entry):
        print("Datastore Add Called")
        # Check day of the week depending on how long program has been running
        self.__get_date()

        # Check to see if a log file exists already
        self.__check_file()

        # Add log entry
        self.__add_log_entry(log_entry)

        print("Datastore Add Complete")


