import sys, datetime, os, subprocess, ctypes
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

class User_Input(object):
    """This will be the python user interface to gather check in/out info"""

    barcode = "-2"
    defaultbg = ""
    otherselected = False
    othervisible = False
    isintextbox = False

    def Checking_In(self):
        print("Checking_In Called")
        # Check for null barcode
        if(self.barcode == "-2"):
            return
        # Create LogEvent obj
        logevent = LogEvent()

        # Update LogEvent obj
        logevent.Add_Barcode(self.barcode)
        logevent.Add_Status("--IN --")
        missing_entry = False

        # Get Current date and time
        date_time = datetime.datetime.now()
        logevent.Add_DateTime(date_time)

        # Get Name from text field
        txt = self.txtname.get()
        logevent.Add_Username(txt)
        if txt == "":
            self.txtname.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            missing_entry = True

        # Get ECN from text field
        txtecn = self.txtecn.get()
        logevent.Add_ECN(txtecn)
        if txtecn == "":
            self.txtecn.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            missing_entry = True

        # Get Tech from drop down
        txttech = self.optionvar.get()
        logevent.Add_Tech(txttech)
        if txttech == 'No Technician':
            self.txttech.configure(highlightbackground="red", highlightcolor="red")
            missing_entry = True

        txtreason = self.reasonoptionvar.get()
        if txtreason == '':
            self.txtreason.configure(highlightbackground="red", highlightcolor="red")
        if self.otherselected:
            txtreason = self.txtother.get()
            if txtreason == '':
                self.txtother.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
                missing_entry = True
        logevent.Add_Comment(txtreason)

        # Missing entry highlight entry fields
        if missing_entry:
            return

        if self.Check_Device_Status():
            answer = messagebox.askyesno("Question","This device has already been checked in, continue?")
            if not answer:
                return

        # Log the LogEvent to file
        Datastore().Add(logevent.Get_Log())
        
        # Save ecn, name, and barcode
        self.Save_JSON(txtecn, txt)

        self.root.destroy()
        return


    def Checking_Out(self):
        print("Checking_Out Called")
        if(self.barcode == "-2"):
            return
        # Create LogEvent obj        
        logevent = LogEvent()
        
        # Update LogEvent obj
        logevent.Add_Barcode(self.barcode)
        logevent.Add_Status("--OUT--")

        missing_entry = False
        
        # Get Current date and time
        date_time = datetime.datetime.now()
        logevent.Add_DateTime(date_time)

        # Get Name from text field
        txt = self.txtname.get()
        logevent.Add_Username(txt)
        if txt == "":
            self.txtname.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            missing_entry = True

        # Get ECN from text field
        txtecn = self.txtecn.get()
        logevent.Add_ECN(txtecn)
        if txtecn == "":
            self.txtecn.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            missing_entry = True
            
        # Get Tech from drop down
        txttech = self.optionvar.get()
        logevent.Add_Tech(txttech)
        if txttech == 'No Technician':
            self.txttech.config(highlightbackground="red", highlightcolor="red")
            missing_entry = True

        # Get Reason from drop down
        txtreason = self.reasonoptionvar.get()
        if self.otherselected:
            txtreason = self.txtother.get()
        logevent.Add_Comment(txtreason)

        # Missing entry highlight entry fields
        if missing_entry:
            return

        if not self.Check_Device_Status():
            answer = messagebox.askyesno("Question","This device has already been checked out, continue?")
            if not answer:
                return

        if not hasattr(self, 'sig_input'):
            self.sig_input = Signature_Input(date_time, txtecn)
            logevent.Add_Signature(self.sig_input.GetFileName())

        # Log the LogEvent to file
        Datastore().Add(logevent.Get_Log())

        # Get Signature if all data is present
        self.Get_Signature()

        # Save ecn, name, and barcode
        self.Save_JSON(txtecn, txt)


    def Check_Device_Status(self):
        ecn = self.txtecn.get()
        if self.jsonDB['Entries'][ecn]:
            last_ix = len(self.jsonDB['Entries'][ecn]) - 1
            status = self.jsonDB['Entries'][ecn][last_ix]['checkIn']
            return status
            

    def Save_JSON(self, ecn, name):
        barcode = self.barcode
        DeviceMaps().Add_mapping(ecn, barcode, name)


    def Get_Signature(self):
        if self.sig_input.isOpen:
            self.Raise_Window()
        else:
            self.sig_input.Run(self.root)
    

    # ON TEXTBOX FOCUS EVENT
    def on_focus_in(self, e):
            print('on_focus_in')
            subprocess.Popen("osk", shell=True)


    def on_focus_out(self, e):
            if not self.isintextbox:
                print('on_focus_out')
                subprocess.call('wmic process where name="osk.exe" delete', shell=True)

    # HOVER EVENTS
    def on_enter(self, e):
        # Hover over button
        e.widget['style'] = "HOV.TButton"
    #
    #
    def on_leave(self, e):
        # Leave Hover over button
        if e.widget is self.exit:
            e.widget['style'] = "BWR.TButton"
        else:
            e.widget['style'] = "BW.TButton"

    def t_on_enter(self, e):
        self.isintextbox = True

    def t_on_leave(self, e):
        self.isintextbox = False
    # END HOVER EVENTS


    # DROPDOWN CHANGES
    def Option_change(self, *args):
        #subprocess.call('wmic process where name="osk.exe" delete', shell=True)
        print("tech: {0}: ".format(self.optionvar.get()))
    #        
    #
    def Reason_change(self, *args):
        #subprocess.call('wmic process where name="osk.exe" delete', shell=True)
        print("reason: {0}: ".format(self.reasonoptionvar.get()))
        reasonName = self.reasonoptionvar.get()
        tempReason = "Reason for visit:"
        self.lblreason.config(text = tempReason)
        if reasonName == "Other":
            self.otherselected = True
            if not self.othervisible:
                self.lblother['text'] = "Other:"
                self.txtother.grid(row=5, column=1, pady=(5,25), padx=(0,20))
                self.othervisible = True
        else:
            self.otherselected = False
            if self.othervisible:
                self.lblother['text'] = ""
                self.txtother.grid_remove()
                self.othervisible = False
    # END DROPDOWN CHANGES


    def __init__(self, barcode, root):
        print("UI Start Called")

        self.jsonDB = DeviceMaps().jsonMap
        self.dcOnlyDB = DeviceMaps().dcJsonMaps

        name = tk.StringVar()
        ecn = tk.StringVar()

        for k in self.jsonDB['Mappings']:
            if self.jsonDB['Mappings'][k]['Barcode'] == barcode:
                self.foundMap = self.jsonDB['Mappings'][k]
                name.set(self.foundMap['Name'])
                ecn.set(self.foundMap['ECN'])

        if len(ecn.get()) <= 1:
            for key, v in self.dcOnlyDB.items():
                if v["Barcode"] == barcode:
                    self.foundMap = v
                    ecn.set(self.foundMap['ECN'])
                    if len(name.get()) <= 1:
                        name.set(self.foundMap['Name'])

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

        # UI barcode property
        self.barcode = barcode

        # Setup GUI
        self.root = root
        #self.root.geometry('1200x700')
        self.root.configure(bg=bg_color)
        winWidth = 1080
        scrnWidth = self.root.winfo_screenwidth()
        posRight = int(scrnWidth/2 - winWidth/2)
        posDown = 10
        self.root.geometry("+{}+{}".format(posRight, posDown))
        self.root.bind("<1>", self.on_focus_out)

        #self.root.eval('tk::PlaceWindow . center')

        # Header display for Barcode Data
        self.header = ttk.Label(root, text="Barcode:", style="BW.TLabel")
        self.header.grid(row=0, column=0, pady=(25,25), padx=(20,20))
        
        self.valheader = ttk.Label(root, text="{0}".format(barcode), style="BW.TLabel", anchor="w", font=font_small)
        self.valheader.grid(row=0, column=1, pady=(25,25), padx=(0,20))

        # Name Section
        self.lbluser = ttk.Label(root, text="Your Name:", style="BW.TLabel")
        self.lbluser.grid(row=1, column=0, pady=(10,25), padx=(20,20))
        
        self.txtname = tk.Entry(root, textvariable=name)
        self.txtname.configure(font=style_font, width=txt_width)
        self.txtname.bind("<1>", self.on_focus_in)
        self.txtname.bind("<Enter>", self.t_on_enter)
        self.txtname.bind("<Leave>", self.t_on_leave)
        self.txtname.grid(row=1, column=1, pady=(10,25), padx=(0,20))

        # ECN Section
        self.lblecn = ttk.Label(root, text="ECN:", style="BW.TLabel")
        self.lblecn.grid(row=2, column=0, pady=(10,25), padx=(20,20))
        
        self.txtecn = tk.Entry(root, textvariable=ecn)
        self.txtecn.configure(font=style_font, width=txt_width)
        self.txtecn.bind("<1>", self.on_focus_in)
        self.txtecn.bind("<Enter>", self.t_on_enter)
        self.txtecn.bind("<Leave>", self.t_on_leave)
        self.txtecn.grid(row=2, column=1, pady=(10,25), padx=(0,20))

        # Technician Section
        self.lbltech = ttk.Label(root, text="Technician:", style="BW.TLabel")
        self.lbltech.grid(row=3, column=0, pady=(10,25), padx=(20,20))
       
        OPTIONS = ["No Technician", "Mike Delsanto", "Max Young", "Kim Tartarini", "Bill Finizia", "Dan Kemp", "Sal Rafique", "Eric Hansen", "Michael Weigel"]
        self.optionvar = StringVar(root)
        self.optionvar.set(OPTIONS[0])
        
        self.txttech = tk.OptionMenu(root, self.optionvar, *OPTIONS, command=self.Option_change)
        self.txttech.configure(bg='white', font=font_s, width=btn_width)
        self.txttech.grid(row=3, column=1, pady=(10,25), padx=(0,20))
        self.txttech['menu'].config(font=font_s)

        # Reason Section
        self.lblreason = ttk.Label(root, text="Reason for visit:", style="BW.TLabel")
        self.lblreason.grid(row=4, column=0, pady=(10,25), padx=(20,20))
        
        REASON_OPTIONS = ["New Device", "Replace Device", "Turn-In Device", "Hardware Issue/Install", "Software Issue/Install", "Checkout/Checkin Loaner", "Other"]
        self.reasonoptionvar = StringVar(root)
        self.txtreason = tk.OptionMenu(root, self.reasonoptionvar, *REASON_OPTIONS, command=self.Reason_change)
        self.txtreason.configure(bg='white', font=font_s, width=btn_width)
        self.txtreason.grid(row=4, column=1, pady=(10,25), padx=(0,20))
        self.txtreason['menu'].config(font=font_s)
        
        self.lblother = ttk.Label(root, style="BW.TLabel")
        self.lblother['text'] = ""
        self.lblother.grid(row=5, column=0, pady=(5,25), padx=(20,20))

        self.txtother = tk.Entry(root,)
        self.txtother.configure(font=style_font, width=txt_width)
        self.txtother.bind("<1>", self.on_focus_in)
        self.txtother.bind("<Enter>", self.t_on_enter)
        self.txtother.bind("<Leave>", self.t_on_leave)

        # Checkin Section
        self.checkin = ttk.Button(root, text="Checking In", command=self.Checking_In, style="BW.TButton")
        self.checkin.bind("<Enter>", self.on_enter)
        self.checkin.bind("<Leave>", self.on_leave)
        self.checkin.grid(row=6, column=0, pady=(10,25), padx=(20,20), columnspan=2)

        # Checkout Section
        self.checkout = ttk.Button(root, text="Checking Out", command=self.Checking_Out, style="BW.TButton")
        self.checkout.bind("<Enter>", self.on_enter)
        self.checkout.bind("<Leave>", self.on_leave)
        self.checkout.grid(row=7, column=0, pady=(10,25), padx=(20,20), columnspan=2)

        # Exit Section
        self.exit = ttk.Button(root, text="Close", command=self.Exit_Click, style="BWR.TButton")
        self.exit.bind("<Enter>", self.on_enter)
        self.exit.bind("<Leave>", self.on_leave)
        self.exit.grid(row=8, column=0, pady=(10,50), padx=(20,20), columnspan=2)

        self.root.mainloop()


    def Exit_Click(self):
        sys.exit()


    # BRING WINDOW FORWARD
    def Raise_Window(self):
        self.sig_input.tk.lift()
        self.sig_input.tk.attributes("-topmost", True)
    # END BRING WINDOW FORWARD
    

    # CHANGE TTK STYLE
    def Change_Style(self, widget, theme):
        widget['style'] = theme