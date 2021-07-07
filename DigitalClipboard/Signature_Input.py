import sys
import os.path
from Configs import Configs
from os import path
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageDraw
from Datastore import Datastore

class Signature_Input:
    isOpen = False
    isSigned = False

    def __init__(self, date_time, ecn):
        self.date_time = date_time
        self.ecn = ecn
        self.filepath = os.path.join(Configs.sigpath, self.GetFileName())


    def on_closing(self):
        isOpen = False
        self.tk.destroy()


    def press(self, evt):
        self.mousePressed = True
    def release(self, evt):
        self.mousePressed = False


    def on_closing(self):
          self.isOpen = False
          self.tk.destroy()


    def finish(self):
        try:
            if self.isSigned:
                self.isOpen = False
                self.img.save(self.filepath)
                self.root.destroy()
                self.tk.destroy()
        except:
            print("finished")


    # HOVER EVENTS
    def on_enter(self, e):
        # Hover over button
        e.widget.configure(bg='white')
    #
    #
    def on_leave(self, e):
        # Leave Hover over button
        e.widget.configure(bg='white smoke')
    # END HOVER EVENTS


    def move(self, evt):
        x,y = evt.x,evt.y
        if self.mousePressed and isinstance(evt.widget, Canvas):
            if hasattr(self, 'canvwidth'):
                if x >= self.canvwidth or y >= self.canvheight or x <= 0 or y <= 0:
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


    def GetFileName(self):
        return f'{self.ecn}_{self.date_time:%Y-%m-%d_%H.%M.%S}.png'


    def Run(self, root):
        self.isOpen = True
        self.root = root
        bg_color = 'white smoke'
        font_s = tkFont.Font(family="Courier", size=20)
        width_s = 50
        self.canvwidth = 650
        self.canvheight = 480

        self.tk = Tk()
        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.tk.attributes("-topmost", True)

        self.lblHeader = Label(self.tk, text="Sign Below", font=font_s, width=width_s)
        self.lblHeader.grid(row=0, column=1, columnspan=3, pady=10, padx=50)

        self.cvs = Canvas(self.tk, width=self.canvwidth, height=self.canvheight, bg='white')
        self.cvs.grid(row=1, column=1)

        self.img = Image.new('RGB',(650,480),(255,255,255))
        self.draw = ImageDraw.Draw(self.img)

        self.mousePressed = False
        self.last=None

        self.cvs.bind_all('<ButtonPress-1>', self.press)
        self.cvs.bind_all('<ButtonRelease-1>', self.release)
        self.btnDone = Button(self.tk,text='Submit', command=self.finish, height=2, width=width_s, font=font_s, bg='white smoke', relief=GROOVE)
        self.btnDone.bind("<Enter>", self.on_enter)
        self.btnDone.bind("<Leave>", self.on_leave)
        self.btnDone.grid(row=2, column=1, columnspan=3, pady=20, padx=50)

        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.cvs.bind_all('<Motion>', self.move)
        self.tk.mainloop()

