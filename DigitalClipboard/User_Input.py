import sys, datetime, os, subprocess, ctypes, re
from time import sleep
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
from Datastore import Datastore
from LogEvent import LogEvent
from Signature_Input import Signature_Input
from DeviceMaps import DeviceMaps
from Common import Logger
from Common import LogTypeString as lts

class User_Input(object):
    """Window for collecting check-in/check-out info"""

    barcode = "-2"          # default/null value for the scanned barcode num
    isintextbox = False     # whether cursor is hovering over a text input field
    isDestroyed = False     # whether User_Input window is closed (via button)

    def Checking_In(self):
        #Logger.Add("Checking_In Called", lts.GEN)

        # Check for null barcode
        if(self.barcode == "-2"):
            return False
        # Create LogEvent obj
        logevent = LogEvent()

        # Update LogEvent obj
        logevent.Add_Barcode(self.barcode)
        logevent.Add_Status("--IN --")
        missing_entry = False

        # Get current date and time for logging.
        date_time = datetime.datetime.now()
        logevent.Add_DateTime(date_time)

        # Get Name from text field
        txt = self.txtname.get()
        logevent.Add_Username(txt)
        
        # Validate Name Field
        missing_entry = self.ValidateName(missing_entry)

        # Get ECN from text field
        txtecn = self.txtecn.get()
        logevent.Add_ECN(txtecn)
        missing_entry = self.ValidateECN(missing_entry)

        # Get Tech from drop down
        txttech = self.optionvar.get()
        logevent.Add_Tech(txttech)
        missing_entry = self.ValidateTech(missing_entry)

        # Get Reason
        txtreason = self.reasonoptionvar.get()
        if txtreason == '':
            self.txtreason.configure(highlightbackground="red", highlightcolor="red")
            missing_entry = True
        else:
            self.txtreason.configure(highlightbackground="white", highlightcolor="white")

        # Get Notes if empty flag else add it to reason
        if txtreason == 'Other':
            txtreason = self.txtother.get()
            missing_entry = self.ValidateReason(missing_entry)
        else:
            txtreason = "{0} : {1}".format(txtreason, self.txtother.get())

        logevent.Add_Comment(txtreason)

        # Missing entry highlight entry fields
        if missing_entry:
            return False

        if self.Check_Device_Status() is True:
            answer = messagebox.askyesno("Question","This device has already been checked in, continue?")
            if not answer:
                return

        # Log the LogEvent to file
        Datastore().Add(logevent.Get_Log())
        
        # Save ecn, name, and barcode
        self.Save_JSON(txtecn, txt, True)

        self.root.destroy()
        return True


    def Checking_Out(self):
        #Logger.Add("Checking_Out Called", lts.GEN)

        if(self.barcode == "-2"):
            return False
        # Create LogEvent obj        
        logevent = LogEvent()
        
        # Update LogEvent obj
        logevent.Add_Barcode(self.barcode)
        logevent.Add_Status("--OUT--")

        missing_entry = False
        
        # Get current date and time for logging.
        date_time = datetime.datetime.now()
        logevent.Add_DateTime(date_time)

        # Get Name from text field
        txt = self.txtname.get()
        logevent.Add_Username(txt)
        missing_entry = self.ValidateName(missing_entry)

        # Get ECN from text field
        txtecn = self.txtecn.get()
        logevent.Add_ECN(txtecn)
        missing_entry = self.ValidateECN(missing_entry)
            
        # Get Tech from drop down
        txttech = self.optionvar.get()
        logevent.Add_Tech(txttech)
        missing_entry = self.ValidateTech(missing_entry)

        # Get Reason from drop down
        txtreason = self.reasonoptionvar.get()
        if txtreason == 'Other':
            txtreason = self.txtother.get()
            missing_entry = self.ValidateReason(missing_entry)
        logevent.Add_Comment(txtreason)

        # Missing entry highlight entry fields
        if missing_entry:
            return False

        if self.Check_Device_Status() is False:
            answer = messagebox.askyesno("Question","This device has already been checked out, continue?")
            if not answer:
                return

        if not hasattr(self, 'sig_input'):
            self.sig_input = Signature_Input(date_time, txtecn)
            logevent.Add_Signature(self.sig_input.GetFileName())

        # Log the LogEvent to file
        Datastore().Add(logevent.Get_Log())

        # Get signature from the user if all required data is present
        self.Get_Signature()

        # Save ecn, name, and barcode
        self.Save_JSON(txtecn, txt, False)


    # Checks the name field for length and valid characters
    def ValidateName(self, status):
        txt = self.txtname.get()

        if len(txt) < 2 or len(txt) > 26:
            self.txtname.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            messagebox.showwarning("Name Warning", "Please enter a valid name between 2 and 26 characters long.")
            return True
        
        valid = re.compile('^([a-zA-Z- ])*\w+$')
        match = valid.match(txt)
        if match:
            print("Regex:", match.group(), match.groups())

        if not bool(re.match('^([a-zA-Z- ])*\w+$', txt)):
            self.txtname.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            messagebox.showwarning("Name Warning", "Please enter a valid name using only alphabet characters(A-Z).")
            return True

        self.txtname.config(highlightthickness=0)
        return status


    # Checks ECN field for length and valid characters
    def ValidateECN(self, status):
        txtecn = self.txtecn.get()

        if len(txtecn) < 4 or len(txtecn) > 6:
            self.txtecn.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            messagebox.showwarning("ECN Warning", "Please enter a valid ECN between 4 and 6 characters long.")
            return True

        if not txtecn.isnumeric():
            self.txtecn.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            messagebox.showwarning("ECN Warning", "Please enter a valid ECN using 0 to 9 without letters.")
            return True

        self.txtecn.config(highlightthickness=0)
        return status


    # Checks the tech dropdown has been changed.
    def ValidateTech(self, status):
        txttech = self.optionvar.get()
        if txttech == 'No Technician':
            self.txttech.config(highlightbackground="red", highlightcolor="red")
            return True

        self.txttech.config(highlightbackground="white", highlightcolor="white")
        return status


    # Checks the other/notes field for an entry.
    def ValidateReason(self, status):
        txtreason = self.txtother.get()
        if len(txtreason) == 0 or len(txtreason) > 50:
            self.txtother.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            messagebox.showwarning("Note Warning", "Please check the note field.\nIt cannot be empty if \"Other\" is selected for the Reason dropdown menu.\nIt also cannot exceed 50 characters in length.")
            return True

        self.txtother.config(highlightbackground="white", highlightcolor="white")
        return status


    # Checks to see if this device has been checked in/out already.
    def Check_Device_Status(self):
        ecn = self.txtecn.get()
        if ecn in self.deviceMaps.keys():
            return self.deviceMaps[ecn]["CheckedIn"]
            

    # Add the given device to the local/remote JSON DBs.
    def Save_JSON(self, ecn, name, checkedin):
        barcode = self.barcode
        self.deviceMapsClass.Add_mapping(ecn, barcode, name, checkedin)


    # Open (or focus) the signature input window to complete checkout.
    def Get_Signature(self):
        if self.sig_input.isOpen:
            self.Raise_Window()
        else:
            self.sig_input.Run(self.root)
    

    # Open the touch keyboard when a text field is focused/clicked.
    def on_focus_in(self, e):
        #Logger.Add('on_focus_in', lts.GEN)
        subprocess.Popen("osk", shell=True)


    # Close the touch keyboard when a text input field is unfocused and the
    # cursor is not hovering over any text input field.
    def on_focus_out(self, e):
        if not self.isintextbox:
            #Logger.Add('on_focus_out', lts.GEN)
            subprocess.call('wmic process where name="osk.exe" delete', shell=True)


    # Change how buttons look when hovered over.
    def on_enter(self, e):
        # Hover over button
        e.widget['style'] = "HOV.TButton"


    # Change button style back to normal when a button is not being hovered
    # over.
    def on_leave(self, e):
        # Leave Hover over button
        if e.widget is self.exit:
            e.widget['style'] = "BWR.TButton"
        else:
            e.widget['style'] = "BW.TButton"


    # Record that the cursor is hovering over a text input field.
    def t_on_enter(self, e):
        self.isintextbox = True


    # Record that the cursor is NOT hovering over a text input field.
    def t_on_leave(self, e):
        self.isintextbox = False
        
    
    # Completely closes application
    def Exit_Click(self):
        # Set isDestroyed so that the main digital clipboard loop exits after close button pressed.
        self.isDestroyed = True
        Logger.Add("Closing", lts.GEN)
        subprocess.call('wmic process where name="osk.exe" delete', shell=True)
        self.root.destroy()
        return


    # Brings signature pane to front.
    def Raise_Window(self):
        self.sig_input.tk.lift()
        self.sig_input.tk.attributes("-topmost", True)
    

    # MAIN ENTRY POINT
    def Run(self):
        # Loop on GUI
        self.root.mainloop()


    # GUI
    def __init__(self, barcode, root):
        Logger.Add("UI Start Called", lts.GEN)

        # store values
        self.barcode = barcode
        self.root = root

        # GET Mapping Data
        self.deviceMapsClass = DeviceMaps()
        self.deviceMaps = self.deviceMapsClass.deviceMaps

        # Init Textbox Variables
        self.name = tk.StringVar()
        self.ecn = tk.StringVar()

        # Pre-fill Name and ECN if the barcode already exists in the JSON DB.
        for v in self.deviceMaps.values():
            if v['Barcode'] == barcode:
                self.name.set(v['Name'])
                self.ecn.set(v['ECN'])
                break

        # Styles / Sizing / Colors
        bg_color = 'white smoke'
        width_s = 30
        btn_width = 30
        txt_width = 30
        font_s = tkFont.Font(family="Courier", size=15)
        font_small = tkFont.Font(family="Courier", size=14)
        style_font = ('Courier', 16)
        self.style = ttk.Style()
        self.style.configure('.', foreground="black", background=bg_color, font=style_font)
        self.style.configure("BW.TLabel", width=width_s, anchor="e")
        self.style.configure("BW.TEntry", width=width_s)
        self.style.configure("ERROR.TEntry", width=width_s)
        self.style.configure("BW.TButton", height=2, width=width_s, relief=GROOVE)
        self.style.configure("BWR.TButton", background="black", height=2, width=width_s, relief=GROOVE)
        self.style.configure("HOV.TButton", background="white", height=2, width=width_s, relief=GROOVE)

        # UI ELEMENTS START HERE
        self.root.title = "Digital Clipboard"

        self.root.configure(bg=bg_color)
        self.root.state('zoomed')
        self.root.bind("<1>", self.on_focus_out)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.columnconfigure(2, weight=3)
        self.root.columnconfigure(3, weight=1)

        # Header display for Barcode Data
        self.header = ttk.Label(root, text="Barcode:", style="BW.TLabel")
        self.header.grid(row=0, column=1, pady=(25,25), padx=(20,20), sticky=E)
        
        self.valheader = ttk.Label(root, text="{0}".format(barcode), style="BW.TLabel", anchor="w", font=font_small)
        self.valheader.grid(row=0, column=2, pady=(25,25), padx=(25,20), sticky=W)

        # Name Section
        self.lbluser = ttk.Label(root, text="Your Name (First Last):", style="BW.TLabel")
        self.lbluser.grid(row=1, column=1, pady=(10,25), padx=(20,20), sticky=E)
        
        self.txtname = tk.Entry(root, textvariable=self.name)
        self.txtname.configure(font=style_font, width=txt_width)
        self.txtname.bind("<1>", self.on_focus_in)
        self.txtname.bind("<Enter>", self.t_on_enter)
        self.txtname.bind("<Leave>", self.t_on_leave)
        self.txtname.grid(row=1, column=2, pady=(10,25), padx=(20,20), sticky=W)

        # ECN Section
        self.lblecn = ttk.Label(root, text="ECN:", style="BW.TLabel")
        self.lblecn.grid(row=2, column=1, pady=(10,25), padx=(20,20), sticky=E)
        
        self.txtecn = tk.Entry(root, textvariable=self.ecn)
        self.txtecn.configure(font=style_font, width=txt_width)
        self.txtecn.bind("<1>", self.on_focus_in)
        self.txtecn.bind("<Enter>", self.t_on_enter)
        self.txtecn.bind("<Leave>", self.t_on_leave)
        self.txtecn.grid(row=2, column=2, pady=(10,25), padx=(20,20), sticky=W)

        # Technician Section
        self.lbltech = ttk.Label(root, text="Technician:", style="BW.TLabel")
        self.lbltech.grid(row=3, column=1, pady=(10,25), padx=(20,20), sticky=E)

        #
        # This is where you would ADD/REMOVE for the Technician Name Dropdown
        self.OPTIONS = ["No Technician", "Mike Delsanto", "Max Young", "Kim Tartarini", "Bill Finizia", "Dan Kemp", "Sal Rafique", "Eric Hansen", "Michael Weigel"]
        self.optionvar = StringVar(root)
        self.optionvar.set(self.OPTIONS[0])
        
        self.txttech = tk.OptionMenu(root, self.optionvar, *self.OPTIONS)
        self.txttech.configure(bg='white', font=font_s, width=btn_width)
        self.txttech.grid(row=3, column=2, pady=(10,25), padx=(20,20), sticky=W)
        self.txttech['menu'].config(font=font_s)

        # Reason Section
        self.lblreason = ttk.Label(root, text="Reason for visit:", style="BW.TLabel")
        self.lblreason.grid(row=4, column=1, pady=(10,25), padx=(20,20), sticky=E)
        
        #
        # This is where you would ADD/REMOVE for the Reason Dropdown
        self.REASON_OPTIONS = ["New Device", "Replace Device", "Turn-In Device", "Hardware Issue/Install", "Software Issue/Install", "Checkout/Checkin Loaner", "Other"]
        self.reasonoptionvar = StringVar(root)
        self.txtreason = tk.OptionMenu(root, self.reasonoptionvar, *self.REASON_OPTIONS)
        self.txtreason.configure(bg='white', font=font_s, width=btn_width)
        self.txtreason.grid(row=4, column=2, pady=(10,25), padx=(20,20), sticky=W)
        self.txtreason['menu'].config(font=font_s)
        
        self.lblother = ttk.Label(root, text="Notes:", style="BW.TLabel")
        self.lblother.grid(row=5, column=1, pady=(5,25), padx=(20,20), sticky=E)

        self.othervar = tk.StringVar()
        self.txtother = tk.Entry(root, textvariable=self.othervar)
        self.txtother.configure(font=style_font, width=txt_width)
        self.txtother.bind("<1>", self.on_focus_in)
        self.txtother.bind("<Enter>", self.t_on_enter)
        self.txtother.bind("<Leave>", self.t_on_leave)
        self.txtother.grid(row=5, column=2, pady=(10,25), padx=(20,20), sticky=W)

        # Checkin button
        self.checkin = ttk.Button(root, text="Checking In", command=self.Checking_In, style="BW.TButton")
        self.checkin.bind("<Enter>", self.on_enter)
        self.checkin.bind("<Leave>", self.on_leave)
        self.checkin.grid(row=6, column=2, pady=(10,25), padx=(20,20), columnspan=1, sticky=W)

        # Checkout button
        self.checkout = ttk.Button(root, text="Checking Out", command=self.Checking_Out, style="BW.TButton")
        self.checkout.bind("<Enter>", self.on_enter)
        self.checkout.bind("<Leave>", self.on_leave)
        self.checkout.grid(row=7, column=2, pady=(10,25), padx=(20,20), columnspan=1, sticky=W)

        # Close/Exit button
        self.exit = ttk.Button(root, text="Close", command=self.Exit_Click, style="BWR.TButton")
        self.exit.bind("<Enter>", self.on_enter)
        self.exit.bind("<Leave>", self.on_leave)
        self.exit.grid(row=8, column=2, pady=(10,50), padx=(20,20), columnspan=1, sticky=W)
