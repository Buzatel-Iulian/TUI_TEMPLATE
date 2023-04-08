import curses
import sys
from TUI_UTIL import *


Interface = Tui()
menu1 = Menu(15, 15, 5, 5, "a")
menu2 = Menu(20, 20, 50, 20, "b", True)
menu3 = Menu(6, 15, 50, 15, "c")
label1 = Label("LabelTest")
labelb = Label("BeginLabelTest")
labele = Label("EndLabelTest")
text1 = Text("Original")
toggle1 = Toggle("Check")
button1 = Button("test", lambda : Interface.STATUS.update("Click !"))
button2 = Button("test again", lambda : Interface.STATUS.update("And Clicked again !"))
button3 = Button("test scale & text crooooooooop", lambda : Interface.STATUS.update("Button"))
num1 = Numeric("number", 5)
num2 = Numeric("number1", 5)
num3 = Numeric("number2", 5)
num4 = Numeric("number3", 5)
num5 = Numeric("number4", 5)
num6 = Numeric("number5", 5)
num7 = Numeric("number6", 5)
menu1.add(labelb)
menu1.add(button1)
menu1.add(toggle1)
menu1.add(label1)
menu1.add(text1)
menu1.add(button2)
menu1.add(labele)
menu2.add(button3)
menu3.add(num2)
menu3.add(num3)
menu3.add(num4)
menu3.add(num5)
menu3.add(num6)
menu3.add(num7)
Interface.addMenu(menu1)
Interface.addMenu(menu2)
Interface.addMenu(menu3)
Interface.start()
