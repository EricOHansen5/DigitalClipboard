# Digital Clipboard is a digital alternative to a hand written clipboard
# that logs in and out entries of computer/device assets

# Author: Eric Hansen

from Main import Main
from Common import Logger, LogTypeString as lts
import datetime

Logger.Add("Hello, welcome to the USARIEM Digital Clipboard.", lts.GEN)
Logger.Add(datetime.datetime.now(), lts.GEN)
main = Main()

main.Run()

