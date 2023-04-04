import curses
import sys
from TUI_UTIL import *


Interface = Tui()
menu1 = Menu(5, 15, 5, 5, "a")
menu2 = Menu(20, 20, 50, 20, "b", True)
button1 = Button("test", lambda : Interface.STATUS.update("Click !"))
button2 = Button("test again", lambda : Interface.STATUS.update("And Clicked again !"))
button3 = Button("test scale & text crooooooooop", lambda : Interface.STATUS.update("Button"))
menu1.addButton(button1)
menu1.addButton(button2)
menu2.addButton(button3)
Interface.addMenu(menu1)
Interface.addMenu(menu2)
Interface.start()
