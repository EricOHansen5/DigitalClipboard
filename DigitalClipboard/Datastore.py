import os.path
from os import path
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import datetime

class Datastore(object):
    """description of class"""
    monday_date = datetime.datetime.today()  - datetime.timedelta(days=datetime.datetime.today().weekday() % 7)
    date_format = f'{monday_date:%Y-%m-%d}.log'

    # Share Drive
    dirpath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Logs\\"
    sigpath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Logs\\Signatures\\"
    checkpath = "\\\\riemfs01\\X\\"
    filename = os.path.join(dirpath, date_format)
    
    # Local Drive
    desktoppath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    localpath = os.path.join(desktoppath, "DC_Logs")
    localfilename = os.path.join(localpath, date_format)

    isuselocal = False

    def __get_date(self):
        # Get the date for this weeks monday (start of week)
        self.monday_date = datetime.datetime.today()  - datetime.timedelta(days=datetime.datetime.today().weekday() % 7)


    def __set_readonly(self):
        print("Set_Readonly")
        if self.isuselocal:
            os.chmod(self.localfilename, S_IREAD|S_IRGRP|S_IROTH)
        else:
            # Set readonly permissions
            os.chmod(self.filename, S_IREAD|S_IRGRP|S_IROTH)


    def __set_writable(self):
        print("Set_Writable")
        if self.isuselocal:
            os.chmod(self.localfilename, S_IWUSR|S_IREAD)
        else:
            # Set readonly permissions
            os.chmod(self.filename, S_IWUSR|S_IREAD)


    def __check_file(self):
        print("Check_File")
        # Check to see if a log file exists already
        log_exists = path.exists(self.filename)
        local_exists = path.exists(self.localfilename)
        local_dir_exists = path.exists(self.localpath)

        if path.exists(self.checkpath):
            self.isuselocal = False
            # If file doesn't exist create it
            if log_exists is False:
                log_file = open(self.filename, "w+")
                log_file.close()

                # Change permissions on file to read-only
                self.__set_readonly()
        else:
            self.isuselocal = True
            if local_exists is False:
                if local_dir_exists is False:
                    os.mkdir(self.localpath)
                log_file = open(self.localfilename, "w+")
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
            log_file = open(self.localfilename, "a+")
        else:
            # Append to log file
            log_file = open(self.filename, "a+")
        
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


