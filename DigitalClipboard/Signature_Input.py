import sys
import os.path
from Configs import Configs
from os import path
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageDraw
from Datastore import Datastore

class Signature_Input:
    """Window in which the customer draws their signature"""

    isOpen = False
    isSigned = False

    def __init__(self, date_time, ecn):
        self.date_time = date_time
        self.ecn = ecn
        self.filepath = os.path.join(Configs.sigpath, self.GetFileName())


    # When the signature input window is X'd out, remove the window and ensure
    # other windows (namely user input window) can see that the signature
    # input window is now closed.
    def on_closing(self):
        isOpen = False
        self.tk.destroy()


    # Record that the user is drawing.
    def press(self, evt):
        self.mousePressed = True


    # Record that the user is not drawing.
    def release(self, evt):
        self.mousePressed = False


    # When the signature input window is X'd out, remove the window and ensure
    # other windows (namely user input window) can see that the signature
    # input window is now closed.
    def on_closing(self):
        self.isOpen = False
        self.tk.destroy()


    # Submit/save the image if something's been drawn, then close the signature
    # input window.
    def finish(self):
        try:
            if self.isSigned:
                self.isOpen = False
                self.img.save(self.filepath)
                self.root.destroy()
                self.tk.destroy()
        except:
            print("finished")


    # Remove all drawn lines.
    def clear(self):
        self.cvs.delete("all")
        self.isSigned = False
        self.last = None


    # Change how buttons look when hovered over.
    def on_enter(self, e):
        # Hover over button
        e.widget.configure(bg='white')


    # Change button style back to normal when a button is not being hovered
    # over.
    def on_leave(self, e):
        # Leave Hover over button
        e.widget.configure(bg='white smoke')


    # Default color of "Clear" button.
    def on_leave_clear(self, e):
        e.widget.configure(bg='rosybrown1')


    # Draw a point-to-point line for every mouse movement, or simply mark a
    # point at "last" if there is no other point to connect to.
    def move(self, evt):
        x,y = evt.x,evt.y
        if self.mousePressed and isinstance(evt.widget, Canvas):
            if hasattr(self, 'canvwidth'):
                if x >= self.cvs.winfo_width() or y >= self.cvs.winfo_height() or x <= 0 or y <= 0:
                    return

            if self.last is None:
                self.last = (x,y)
                return
            self.draw.line(((x,y),self.last), (0,0,0))
            self.cvs.create_line(x,y,self.last[0],self.last[1])
            self.last = (x,y)
            self.isSigned = True
        else:
            self.last = (x,y)


    # Generate a filename for the signature image file.
    def GetFileName(self):
        return f'{self.ecn}_{self.date_time:%Y-%m-%d_%H.%M.%S}.png'


    # Control flow for when the signature input window is run.
    def Run(self, root):
        self.isOpen = True
        self.root = root
        bg_color = 'white smoke'
        font_s = tkFont.Font(family="Courier", size=20)
        width_s = 50

        self.tk = Tk()
        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.tk.attributes("-topmost", True)
        self.tk.state('zoomed')
        self.tk.update_idletasks()      # keeps winfo_width/winfo_height accurate

        self.tk.columnconfigure(0, weight=1)
        self.tk.columnconfigure(1, weight=14)
        self.tk.columnconfigure(2, weight=1)

        self.tk.rowconfigure(0, weight=1)
        self.tk.rowconfigure(1, weight=10)
        self.tk.rowconfigure(2, weight=1)

        # Make the canvas fit the window, but with room for the "Submit" button.
        self.canvwidth = self.tk.winfo_width()
        self.canvheight = self.tk.winfo_height() - self.tk.winfo_height() // 5

        # Instructions atop canvas
        self.lblHeader = Label(self.tk, text="Sign Below", font=font_s, width=width_s, height=1)
        self.lblHeader.grid(row=0, column=1, columnspan=1, ipady=20, padx=50, sticky=S)

        # Drawing area (canvas)
        self.cvs = Canvas(self.tk, bg='white')
        self.cvs.grid(row=1, column=1, sticky=NSEW)

        self.img = Image.new('RGB',(self.canvwidth, self.canvheight),(255,255,255))
        self.draw = ImageDraw.Draw(self.img)

        # Nothing pressed or drawn yet.
        self.mousePressed = False
        self.last=None

        self.cvs.bind_all('<ButtonPress-1>', self.press)
        self.cvs.bind_all('<ButtonRelease-1>', self.release)

        # Clear/erase button
        self.btnClear = Button(self.tk, text="Clear", command=self.clear, height=2, width=width_s, font=font_s, bg='rosybrown1', relief=GROOVE)
        self.btnClear.bind("<Enter>", self.on_enter)
        self.btnClear.bind("<Leave>", self.on_leave_clear)
        self.btnClear.grid(row=2, column=1, pady=20, padx=10, sticky=W)

        # Submit button
        self.btnDone = Button(self.tk,text='Submit', command=self.finish, height=2, width=width_s, font=font_s, bg='white smoke', relief=GROOVE)
        self.btnDone.bind("<Enter>", self.on_enter)
        self.btnDone.bind("<Leave>", self.on_leave)
        self.btnDone.grid(row=2, column=1, pady=20, padx=10, sticky=E)

        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)   # when X'd out
        self.cvs.bind_all('<Motion>', self.move)    # bind mouse movement
        
        # Loop/block indefinitely, awaiting input/events (until closed).
        self.tk.mainloop()

