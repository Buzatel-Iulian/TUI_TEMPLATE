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
    cleared = True
    screen = curses.initscr()
    screen.clear()
    STATUS = Status(screen, "Use arrow keys to go up and down, Press enter to select a choice")
    count = 0
    interface = Structure(screen)
    w_clean = {}
    for i in range(len(interface.interface)): w_clean[i]=False
    p_w_clean = {}
    for i in range(len(interface.interface)): p_w_clean[i]=False

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
        #w_clean = False
        #cleared = False
        max_y, max_x = stdscr.getmaxyx()
        prev_h_menu = h_menu
        prev_highlight = highlight
        if prev_max_x != max_x or prev_max_y != max_y :
            screen.clear()
            interface.start()
            #interface.refresh()
            cleared = True
            prev_max_y = max_y
            prev_max_x = max_x
            STATUS.show()

        count += 1
        #STATUS.show()
        if cursor == "   ":
            cursor = ">> "
        else :
            cursor = "   "
        #getting pressed key -> char
        try:
            char = screen.getch()
        except:
            pass
        #screen.clear()

        if char == curses.KEY_UP:
            if interface.interface[h_menu]["type"][0:8] == "vertical":
                highlight = len(interface.interface[h_menu]["widgets"]) if highlight <= 1 else highlight - 1
            else:
                h_menu = len(interface.interface)-1 if h_menu == 0 else h_menu - 1
            screen.refresh()
        elif char == curses.KEY_DOWN:
            if interface.interface[h_menu]["type"][0:8] == "vertical":
                highlight = 1 if highlight >= len(interface.interface[h_menu]["widgets"]) else highlight + 1
            else:
                h_menu = 0 if h_menu == len(interface.interface)-1 else h_menu + 1
            screen.refresh()
        elif char == curses.KEY_RIGHT:
            if interface.interface[h_menu]["type"][0:8] == "vertical":
                h_menu = 0 if h_menu == len(interface.interface)-1 else h_menu + 1
            else:
                highlight = 1 if highlight >= len(interface.interface[h_menu]["widgets"]) else highlight + 1
            screen.refresh()
        elif char == curses.KEY_LEFT:
            if interface.interface[h_menu]["type"][0:8] == "vertical":
                h_menu = len(interface.interface)-1 if h_menu == 0 else h_menu - 1
            else:
                highlight = len(interface.interface[h_menu]["widgets"]) if highlight <= 1 else highlight - 1
            screen.refresh()

        elif char == ord("\n"):  # Enter
            text = read(screen)
            #screen.clear()
            #cleared = True
            prev_max_x = 0 # (dirty) use to clear and mark cleared at same time
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
            if char != -1:
                if chr(char) in interface.fast_keys :
                    h_menu = interface.fast_keys[chr(char)]
                else :
                    STATUS.update("Character pressed ( %s / %r ) is not a program key" % (char, chr(char)))
            screen.refresh()
        
        if highlight > len(interface.interface[h_menu]["widgets"]) :
            highlight = len(interface.interface[h_menu]["widgets"])

        if prev_h_menu != h_menu or highlight != prev_highlight:
            if interface.interface[prev_h_menu]["widgets"][prev_highlight-1]["type"] in ["text"]:
                if p_w_clean[prev_h_menu]:
                    w_clean[prev_h_menu] = True
        #        aux2, aux = interface.interface[prev_h_menu]["win"].getmaxyx()
        #        if len(interface.interface[prev_h_menu]["widgets"][prev_highlight-1]["text"]) > aux :
        #            w_clean = True # NEED TO get rid of all of THIS <<< ^^^
        #cleared = True
        i = 0
        aux = len(interface.interface)
        #for window in interface.interface:
        while i < aux :
            if h_menu == i :
                p_w_clean[i] = print_menu(interface.interface[i], highlight, True, cursor, w_clean[i])
                w_clean[i] = False
            elif prev_h_menu == i:
                w_clean[i] = print_menu(interface.interface[i], highlight, False, cursor, w_clean[i])
            elif cleared :
                w_clean[i] = print_menu(interface.interface[i], highlight, False, cursor, False)
            #w_clean[i] = False
            i = i + 1
        screen.refresh()
        cleared = False

        ad_hline(screen, max_y-1, 0, curses.ACS_HLINE, max_x)
        ad_str(screen, max_y-1, 0, " y/H={} x/W={} frame={} ".format(max_y, max_x, count))

    curses.endwin()

    sys.exit(0)

curses.wrapper(main)