import curses
import time
import sys
from TUI_UTIL import *


Interface = Tui()
menu1 = Menu(15, 15, 5, 5, "a", "Main")
menu2 = Menu(20, 20, 50, 20, "b", scaling = True)
menu3 = Menu(6, 15, 50, 15, "c")
menu4 = Menu(20, 20, 25, 20, "d", scaling = True)
label1 = Label("LabelTest")
labelb = Label("BeginLabelTest")
labele = Label("EndLabelTest")
text1 = Text("Original")
toggle1 = Toggle("Check")
button1 = Button("test", lambda : Interface.STATUS.update("Click !"))
button2 = Button("test again", lambda : Interface.STATUS.update("And Clicked again !"))
button3 = Button("test scale & text crooooooooop", lambda : Interface.STATUS.update("Button"))
num1 = Numeric("number", 5)
num2 = Label("number1")
num3 = Label("number2")
num4 = Numeric("number3", 5)
num5 = Numeric("number4", 5)
num6 = Label("number5")
num7 = Label("number6")
num11 = Numeric("number1", 5)
num12 = Numeric("number2", 5)
num13 = Numeric("number3", 5)
num14 = Numeric("number4", 5)
num15 = Numeric("number5", 5)
num16 = Numeric("number6", 5)
num17 = Numeric("number7", 5)
menu1.add(labelb)
menu1.add(button1)
menu1.add(toggle1)
menu1.add(label1)
menu1.add(text1)
menu1.add(button2)
menu1.add(labele)
menu2.add(button3)
menu2.add(num1)
menu3.add(num2)
menu3.add(num3)
menu3.add(num4)
menu3.add(num5)
menu3.add(num6)
menu3.add(num7)
menu4.add(num11)
menu4.add(num12)
menu4.add(num13)
menu4.add(num14)
menu4.add(num15)
menu4.add(num16)
menu4.add(num17)
Interface.addMenu(menu1)
Interface.addMenu(menu2)
Interface.addMenu(menu3)
Interface.addMenu(menu4)
Interface.start()
aux = True
while Interface.running:
    time.sleep(2)
    if aux:
        aux = False
        num1.text = "Hey"
    else:
        aux = True
        num1.text = "There"
Interface.stop()
