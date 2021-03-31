import sys
import os.path
from os import path
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageDraw
from Datastore import Datastore

class Signature_Input:
    def __init__(self, date_time, ecn):
        self.date_time = date_time
        self.ecn = ecn
        self.filepath = os.path.join(Datastore.sigpath, self.GetFileName())

    def press(self, evt):
        self.mousePressed = True
    def release(self, evt):
        self.mousePressed = False

    def finish(self):
        try:
            self.img.save(self.filepath)
            self.root.destroy()
            self.tk.destroy()
        except:
            print("finished")


    def move(self, evt):
        x,y = evt.x,evt.y
        if self.mousePressed:
            if self.last is None:
                self.last = (x,y)
                return
            self.draw.line(((x,y),self.last), (0,0,0))
            self.cvs.create_line(x,y,self.last[0],self.last[1])
            self.last = (x,y)
        else:
            self.last = (x,y)


    def GetFileName(self):
        return f'{self.ecn}_{self.date_time:%Y-%m-%d_%H.%M.%S}.png'


    def Run(self, root):
        self.root = root
        bg_color = 'white smoke'
        font_s = tkFont.Font(family="Courier", size=20)
        width_s = 50

        self.tk = Tk()
        self.lblHeader = Label(self.tk, text="Sign Below", font=font_s, width=width_s)
        self.lblHeader.pack()

        self.cvs = Canvas(self.tk, width=650,height=480)
        self.cvs.pack()

        self.img = Image.new('RGB',(650,480),(255,255,255))
        self.draw = ImageDraw.Draw(self.img)

        self.mousePressed = False
        self.last=None

        self.cvs.bind_all('<ButtonPress-1>', self.press)
        self.cvs.bind_all('<ButtonRelease-1>', self.release)
        Button(self.tk,text='done',command=self.finish, height=2, width=width_s, font=font_s, relief=GROOVE).pack(pady=(20,20))

        self.cvs.bind_all('<Motion>', self.move)
        self.tk.mainloop()

