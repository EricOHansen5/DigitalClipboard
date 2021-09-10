from User_Input import User_Input
from Configs import Configs
from Logger import Logger
from LogTypeString import LogTypeString as lts
import tkinter as tk
from tkinter import *

def init_ui():
    ui = User_Input("barcode_test", Tk())

    ui.name.set("test name")
    ui.ecn.set("0001")
    ui.optionvar.set(ui.OPTIONS[1])
    ui.reasonoptionvar.set(ui.REASON_OPTIONS[1])
    ui.othervar.set("test note")

    return ui

def test_Checking_In_Pass():
    ui = init_ui()
    
    if ui.Checking_In():
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)

    ui = init_ui()
    ui.reasonoptionvar.set(ui.REASON_OPTIONS[6])

    if ui.Checking_In():
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)


def test_Checking_In_Fail():
    ui = init_ui()

    ui.name.set("test1 name")

    if not ui.Checking_In():
        Logger.Add("PASS", lts.GEN)
    else:
        Logger.Add("FAILED", lts.ERR)

# Run Tests
test_Checking_In_Pass()
test_Checking_In_Fail()