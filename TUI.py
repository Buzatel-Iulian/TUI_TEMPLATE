#! /usr/bin/env python

# A Python port of Example 10 from
# http://www.tldp.org/HOWTO/NCURSES-Programming-HOWTO/keys.html

from TUI_UTIL import *
from TUI_STRUCT import *
import curses
import sys

# Constants
WIDTH = 22
HEIGHT = 10

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
    interface = [
        {
            "name":"MODS",
            "win":curses.newwin(HEIGHT, WIDTH, 1, 2),
            "widgets":[
                {"text":"TESSELATION","type":"checkbox"},
                {"text":"CONTOURS","type":"checkbox"},
                {"text":"MARKS","type":"checkbox"},
                {"text":"IRISES","type":"checkbox"},
            ]
        },
        {
            "name":"USED MODEL",
            "win":curses.newwin(HEIGHT, WIDTH, 1, 23),
            "widgets":[
                {"text":"LOAD","type":"button"},
                {"text":"LOADED MODEL","type":"label"},
                {"text":"MASK_ON","type":"checkbox"},
            ]
        }
    ]

    #screen.clear()
    curses.noecho()
    curses.curs_set(0)
    screen.scrollok(True)
    screen.keypad(True)
    screen.timeout(REFRESH_RATE)
    cursor = "   "
    curses.cbreak()  # Line buffering disabled. pass on everything
    screen.refresh()
    n_menus = len(interface)

    while True:
        max_y, max_x = stdscr.getmaxyx()
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
                highlight = len(interface[h_menu]["widgets"])
            else:
                highlight = highlight - 1
            screen.refresh()
        elif char == curses.KEY_DOWN:
            if highlight >= len(interface[h_menu]["widgets"]):
                highlight = 1
            else:
                highlight = highlight + 1
            screen.refresh()
        elif char == curses.KEY_RIGHT:
            if h_menu == len(interface)-1:
                h_menu = 0
            else:
                h_menu = h_menu + 1
            screen.refresh()
        elif char == curses.KEY_LEFT:
            if h_menu == 0 :
                h_menu = len(interface)-1
            else:
                h_menu = h_menu - 1
            screen.refresh()

        elif char == ord("\n"):  # Enter
            #ad_str(screen, y, x, "{}".format(screen.getyx()))
            text = read(screen)
            STATUS.update("Given string = " + text)
            #screen.getch()
            #screen.refresh()
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
        for window in interface:
            if h_menu == i :
                print_menu(window, highlight, True, cursor)
            else :
                print_menu(window, highlight, False, cursor)
            i = i + 1
        screen.refresh()

    curses.endwin()

    sys.exit(0)

curses.wrapper(main)