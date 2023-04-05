import curses
import sys
from TUI_UTIL import *


Interface = Tui()
menu1 = Menu(15, 15, 5, 5, "a")
menu2 = Menu(20, 20, 50, 20, "b", True)
label1 = Label("LabelTest")
labelb = Label("BeginLabelTest")
labele = Label("EndLabelTest")
text1 = Text("Original")
toggle1 = Toggle("Check")
button1 = Button("test", lambda : Interface.STATUS.update("Click !"))
button2 = Button("test again", lambda : Interface.STATUS.update("And Clicked again !"))
button3 = Button("test scale & text crooooooooop", lambda : Interface.STATUS.update("Button"))
menu1.add(labelb)
menu1.add(button1)
menu1.add(toggle1)
menu1.add(label1)
menu1.add(text1)
menu1.add(button2)
menu1.add(labele)
menu2.add(button3)
Interface.addMenu(menu1)
Interface.addMenu(menu2)
Interface.start()
