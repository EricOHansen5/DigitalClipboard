import cv2, os.path, sys, tkinter, keyboard, winsound
from os import path
from tkinter import *
from tkinter import messagebox
from pyzbar import pyzbar
from pyzbar.pyzbar import decode, ZBarSymbol
import datetime as date
from User_Input import User_Input

class Main(object):

    def read_barcodes(self, frame):


        #print("Reading Frame")
        barcodes = pyzbar.decode(frame, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
        #print(barcodes)
        result = "-1"

        for barcode in barcodes:
            x, y, w, h = barcode.rect

            # 1
            barcode_info = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # 2
            #font = cv2.FONT_HERSHEY_DUPLEX
            #cv2.putText(frame, barcode_info, (x+6, y-6), font, 2.0, (255, 255, 255), 1)

            # 3
            #with open("barcode_result.txt", mode='a') as file:
                #file.write(date.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " -- " + barcode_info + "\n")
        
            result = barcode_info
            if result != "-1":
                return result
        return result

    def wait_for_barcodes(self):

        try:
            print("wait_for_barcodes called")
            # Initialize results to display
            result = "-1"

            # Gather video capture device
        #    self.camera = cv2.VideoCapture(0)

            # Read frame from capture device
            ret, frame = self.camera.read()
    
            # Loop until barcode found
            while ret:
                ret, frame = self.camera.read()

                # Parse frame for barcode/qr
                result = self.read_barcodes(frame)
        
                # Show camera to screen
                cv2.imshow('Barcode/QR code reader', frame)

                # Wait for barcode/qr code to be parsed from frame
                if (cv2.waitKey(1) & 0xFF == 27) or (result != "-1"):
                    winsound.PlaySound(r'C:\Windows\Media\tada.wav', winsound.SND_FILENAME)
                    self.root = Tk()
                    ui = User_Input(result, self.root)
                    result = "-1"

    
            # Release the camera and close gui window for camera
            camera.release()
            cv2.destroyAllWindows()

            # Return barcode results
            return result
        except Exception as e:
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(e.args[0]))
            return None

    def Run(self):
        #filename = '\\\\riemfs01\\X\\AutomationTools\\pypi\\DigitalClipboard\\logs\\logs.txt'
        #if path.exists(filename) == False:
        #    print("log file doesn't exist")
        #sys.stdout = open(filename, 'a')
        print("\n\n---- Digital Clipboard ----")

        try:
            self.camera = cv2.VideoCapture(0)
            #while True:
                #print("Run Called")

                #while True:
            barcode = self.wait_for_barcodes()

            #    if(barcode != "-1"):
                    # Print qr/barcode scanned
                    #print("qr/barcode scan:", barcode)

                    # Create Tkinter Window
                  #  root = Tk()

                    # Start the UI to handle barcode/qr scan
                 #   ui = User_Input(barcode, root)

            #sys.stdout.close()
        except ValueError as ve:
            print("Exception: ", ValueError)
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(ve.args[0]))
            #sys.stdout.close()
        except Exception as e:
            print("Unexpected Exception: ", sys.exc_info()[0])
            messagebox.showerror(title='ERROR', message='Error in Main.wait_for_barcodes:\n\n"{0}"'.format(e.args[0]))
            #sys.stdout.close()
            raise




