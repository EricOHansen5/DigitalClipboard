# Digital Clipboard is a digital alternative to a hand written clipboard
# that logs in and out entries of computer/device assets

# Author: Eric Hansen
import sys, cv2, winsound, tkinter, numpy as np, datetime as date
import time
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
            # Get video device
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            # Read frame from capture device
            ret, frame = self.camera.read()

            self.isDestroyed = False
            self.oldFrame = frame

            # Loop until barcode found
            while not self.isDestroyed:
                # Read frame from capture device
                ret, frame = self.camera.read()
                if frame is None:
                    continue
                else:
                    frame = cv2.resize(frame, (1920, 1080), cv2.INTER_LINEAR)
                    self.oldFrame = frame

                # Initialize results to display
                result = "-1"

                # Parse frame for barcode/qr
                result = self.read_barcodes(frame)
        
                # Show camera to screen
                cv2.namedWindow('Barcode Reader', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Barcode Reader', frame)
                cv2.moveWindow('Barcode Reader', 0, 0)

                # Wait for barcode/qr code to be parsed from frame
                if (cv2.waitKey(1) & 0xFF == 27) or (result != "-1"):
                    #Logger.Add("Found Barcode: " + result, lts.GEN)
                    winsound.PlaySound(r'C:\Windows\Media\tada.wav', winsound.SND_FILENAME)
                    self.root = Tk()
                    ui = User_Input(result, self.root)
                    if ui.isDestroyed:
                        self.isDestroyed = True
                        break
                    ret, frame = self.camera.read()
                    
            # Release the camera and close gui window for camera
            self.camera.release()
            cv2.destroyAllWindows()
            Logger.Add("Finished Cleaning Up", lts.GEN)

        except Exception as e:
            Logger.Add("Exception - Wait for Barcode: " + str(sys.exc_info()[0]), lts.ERR)
            Logger.Add("\tcont. : " + e.args[0], lts.ERR)
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(e.args[0]))


    def Run(self):
        # Create a string array so that the Logger isn't openning and closing the file for each line written.
        logger = []
        logger.append(("---- Digital Clipboard ----", lts.GEN))
        logger.append((date.datetime.now(), lts.GEN))

        try:
            Logger.AddList(logger)
            if cv2.useOptimized() is False:
                cv2.setUseOptimized(True)
            
            # Wait for barcode to enter camera view
            self.wait_for_barcodes()

        except ValueError as ve:
            Logger.Add("Exception: " + ValueError, lts.ERR)
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(ve.args[0]))
            input("Enter to exit")
        except Exception as e:
            Logger.Add("Unknown Exception: " + str(sys.exc_info()[0]), lts.ERR)
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(e.args[0]))
            input("Enter to exit")
            raise


DigitalClipboard().Run()