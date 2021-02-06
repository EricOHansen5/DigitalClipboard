import sys
from tkinter import *
import tkinter.font as tkFont
from Datastore import Datastore
from LogEvent import LogEvent

class User_Input(object):
    """This will be the python user interface to gather check in/out info"""

    barcode = "-2"
    defaultbg = ""
    
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
        if txttech == "":
            self.txttech.config(highlightbackground="red", highlightcolor="red", highlighthickness=2)
            missing_entry = True

        # Missing entry highlight entry fields
        if missing_entry:
            return

        # Log the LogEvent to file
        Datastore().Add(logevent.Get_Log())

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
        if txttech == "":
            self.txttech.config(highlightbackground="red", highlightcolor="red", highlighthickness=2)
            missing_entry = True

        # Missing entry highlight entry fields
        if missing_entry:
            return

        # Log the LogEvent to file
        Datastore().Add(logevent.Get_Log())

        self.root.destroy()
        return

    
    def Exit_Click(self):
        sys.exit()


    def on_enter(self, e):
        self.defaultbg = e.widget['background']
        e.widget['background'] = 'white'


    def on_leave(self, e):
        e.widget['background'] = self.defaultbg


    def Option_change(self):
        print("tech: {0}: ".format(self.optionvar.get()))
        techName = self.optionvar.get()
        tempStr = "Technician: [{0}]".format(techName)
        self.lbltech.config(text = tempStr)


    def __init__(self, barcode, root):
        print("UI Start Called")
        bg_color = 'white smoke'
        font_s = tkFont.Font(family="Courier", size=15)
        width_s = 50
        
        # UI barcode property
        self.barcode = barcode

        # Setup GUI
        self.root = root
        self.root.geometry('1000x700')
        self.root.configure(bg=bg_color)

        # Header display for Barcode Data
        self.header = Label(root, text="Device Action:[{0}]".format(barcode), font=font_s)
        self.header.pack(side='top', pady=(30,20))
        self.header.configure(bg=bg_color)
        
        # Name Section
        self.lbluser = Label(root, text="Your Name:", font=font_s)
        self.lbluser.pack(side='top')
        self.lbluser.configure(bg=bg_color)

        self.txtname = Entry(root, width=width_s, font=font_s)
        self.txtname.pack(fill=NONE, side='top', pady=(5,25))

        # ECN Section
        self.lblecn = Label(root, text="ECN:", font=font_s)
        self.lblecn.pack(side='top')
        self.lblecn.configure(bg=bg_color)

        self.txtecn = Entry(root, width=width_s, font=font_s)
        self.txtecn.pack(fill=NONE, side='top', pady=(5,25))

        # Technician Section
        self.lbltech = Label(root, text="Technician: ", font=font_s)
        self.lbltech.pack(side='top')
        self.lbltech.configure(bg=bg_color)

        OPTIONS = ["No Technician", "Mike Delsanto", "Max Young", "Kim Tartarini", "Bill Finizia", "Dan Kemp", "Sal Rafique", "Eric Hansen"]
        self.optionvar = StringVar(root)
        self.optionvar.set(OPTIONS[0])
        self.txttech = OptionMenu(root, self.optionvar, *OPTIONS, command=self.Option_change)
        self.txttech.config(font=font_s, bg='white', width=(int)(width_s*0.75), highlightthickness=1)
        self.txttech.pack(side='top', pady=(5,25))
        # Change font size for popup
        self.menu = self.root.nametowidget(self.txttech.menuname)
        self.menu.config(font=font_s)

        # Checkin Section
        self.checkin = Button(root, text="Checking In", height=2, width=width_s, font=font_s, relief=GROOVE, command=self.Checking_In)
        self.checkin.pack(side='top', pady=(10,20))
        self.checkin.configure(bg=bg_color)
        self.checkin.bind("<Enter>", self.on_enter)
        self.checkin.bind("<Leave>", self.on_leave)

        # Checkout Section
        self.checkout = Button(root, text="Checking Out", height=2, width=width_s, font=font_s, relief=GROOVE, command=self.Checking_Out)
        self.checkout.pack(side='top', pady=(10,20))
        self.checkout.configure(bg=bg_color)
        self.checkout.bind("<Enter>", self.on_enter)
        self.checkout.bind("<Leave>", self.on_leave)

        # Exit Section
        self.exit = Button(root, text="Close", height=2, width=width_s, relief=GROOVE, command=self.Exit_Click, font=font_s)
        self.exit.configure(background='#ffcccc')
        self.exit.pack(side='top', pady=(20,20))
        self.exit.bind("<Enter>", self.on_enter)
        self.exit.bind("<Leave>", self.on_leave)

        self.root.mainloop()