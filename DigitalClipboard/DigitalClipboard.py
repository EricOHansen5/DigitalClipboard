# Digital Clipboard is a digital alternative to a hand written clipboard
# that logs in and out entries of computer/device assets

# Author: Eric Hansen
import sys, cv2, winsound, tkinter, numpy as np, datetime as date
from tkinter import *
from tkinter import messagebox
from Common import Logger, LogTypeString as lts
from pyzbar import pyzbar
from pyzbar.pyzbar import decode, ZBarSymbol
from User_Input import User_Input

class DigitalClipboard(object):
    def read_barcodes(self, frame):
        # Read barcodes QRCODES and CODE128
        barcodes = pyzbar.decode(frame, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
        result = "-1"

        for barcode in barcodes:
            # Create rectangle to display on camera
            x, y, w, h = barcode.rect

            # Decode the barcode
            barcode_info = barcode.data.decode('utf-8')
            barcode_type = barcode.type

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
            result = barcode_info
            if result != "-1":
                return result
        return result


    def wait_for_barcodes(self):
        try:
            #Logger.Add("wait_for_barcodes called", lts.GEN)
            # Initialize results to display
            result = "-1"

            # Read frame from capture device
            ret, frame = self.camera.read()
            #Logger.Add("DEBUG After Read", lts.GEN)

            frame = cv2.resize(frame, (854,480), cv2.INTER_LINEAR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
            #Logger.Add("DEBUG After Resize", lts.GEN)

            # Loop until barcode found
            while ret:
                ret, frame = self.camera.read()

                # Parse frame for barcode/qr
                result = self.read_barcodes(frame)
        
                # Show camera to screen
                cv2.imshow('Barcode/QR code reader', frame)

                # Wait for barcode/qr code to be parsed from frame
                if (cv2.waitKey(1) & 0xFF == 27) or (result != "-1"):
                    #Logger.Add("Found Barcode: " + result, lts.GEN)
                    winsound.PlaySound(r'C:\Windows\Media\tada.wav', winsound.SND_FILENAME)
                    self.root = Tk()
                    ui = User_Input(result, self.root)
                    if ui.isDestroyed:
                        break
                    result = "-1"
    
            # Release the camera and close gui window for camera
            self.camera.release()
            cv2.destroyAllWindows()
            Logger.Add("Finished Cleaning Up", lts.GEN)
            return result

        except Exception as e:
            Logger.Add("Exception - Wait for Barcode: " + sys.exc_info()[0], lts.ERR)
            Logger.Add("\tcont. : " + e.args[0], lts.ERR)
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(e.args[0]))
            return None


    def Run(self):
        Logger.Add("---- Digital Clipboard ----", lts.GEN)
        Logger.Add(date.datetime.now(), lts.GEN)

        try:
            if cv2.useOptimized() is False:
                cv2.setUseOptimized(True)

            #Logger.Add("DEBUG VideoCapture", lts.GEN)

            # Get video device
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            
            #Logger.Add("Got Camera Successfully", lts.GEN)

            # Wait for barcode to enter camera view
            barcode = self.wait_for_barcodes()

        except ValueError as ve:
            Logger.Add("Exception: " + ValueError, lts.ERR)
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(ve.args[0]))
            input("Enter to exit")
        except Exception as e:
            Logger.Add("Unknown Exception: " + sys.exc_info()[0], lts.ERR)
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(e.args[0]))
            input("Enter to exit")
            raise


DigitalClipboard().Run()