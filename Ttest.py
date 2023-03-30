import curses
import sys
from TUI_UTIL import *


Interface = Tui()
menu1 = Menu(5, 15, 5, 5, "a")
button = Button(menu1.win, "test", lambda : Interface.STATUS.update("Click !"))
menu1.addButton(button)
Interface.addMenu(menu1)
Interface.start()
