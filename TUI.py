#! /usr/bin/env python

from TUI_UTIL import *
from TUI_STRUCT import *
import curses
import sys

# Constants

def main(stdscr):
    """ Entry point for example 10
    """
    highlight = 1
    h_menu = 0
    pressed = False

    screen = curses.initscr()
    screen.clear()
    STATUS = Status(screen, "Use arrow keys to go up and down, Press enter to select a choice")
    count = 0
    interface = Structure(screen)

    #screen.clear()
    curses.noecho()
    curses.curs_set(0)
    screen.scrollok(True)
    screen.keypad(True)
    screen.timeout(REFRESH_RATE)
    cursor = "   "
    curses.cbreak()  # Line buffering disabled. pass on everything
    screen.refresh()
    n_menus = len(interface.interface)
    prev_max_y, prev_max_x = stdscr.getmaxyx()

    while True:
        max_y, max_x = stdscr.getmaxyx()
        if prev_max_x != max_x or prev_max_y != max_y :
            screen.clear()
            interface.start()
            
            prev_max_y = max_y
            prev_max_x = max_x

        count += 1
        STATUS.show()
        if cursor == "   ":
            cursor = ">> "
        else :
            cursor = "   "
        #getting pressed key -> char
        try:
            char = screen.getch()
        except:
            pass
        pressed = True if char != -1 else False
        #screen.clear()
        ad_str(screen, max_y-2, 0, " y={} x={} frame={}".format(max_y, max_x, count))

        if char == curses.KEY_UP:
            if highlight <= 1:
                highlight = len(interface.interface[h_menu]["widgets"])
            else:
                highlight = highlight - 1
            screen.refresh()
        elif char == curses.KEY_DOWN:
            if highlight >= len(interface.interface[h_menu]["widgets"]):
                highlight = 1
            else:
                highlight = highlight + 1
            screen.refresh()
        elif char == curses.KEY_RIGHT:
            if h_menu == len(interface.interface)-1:
                h_menu = 0
            else:
                h_menu = h_menu + 1
            screen.refresh()
        elif char == curses.KEY_LEFT:
            if h_menu == 0 :
                h_menu = len(interface.interface)-1
            else:
                h_menu = h_menu - 1
            screen.refresh()

        elif char == ord("\n"):  # Enter
            text = read(screen)
            STATUS.update("Given string = " + text)
        elif char == 27 :
            screen.nodelay(True)
            n = screen.getch()
            if n == -1:
            # Escape was pressed
                screen.nodelay(False)
                break
            screen.nodelay(False)
        else:
            if pressed:
                STATUS.update("Character pressed ( %s / %r ) is not a program key" % (char, chr(char)))
            screen.refresh()

        i = 0
        for window in interface.interface:
            if h_menu == i :
                print_menu(window, highlight, True, cursor)
            else :
                print_menu(window, highlight, False, cursor)
            i = i + 1
        screen.refresh()

    curses.endwin()

    sys.exit(0)

curses.wrapper(main)