
import curses
import sys
# CONSTANTS
REFRESH_RATE = 500 # ms

class Status:
    def __init__(self, elem, stat):
        self.elem = elem
        self.stat = stat
        self.show()
    def update (self, st):
        self.stat = st
        #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        self.show()
    def show(self):
        y, x = self.elem.getmaxyx()
        ad_str(self.elem, 0, 0, self.stat, curses.A_STANDOUT)

def print_menu(menu_win, h_, menu_h, _cursor = "   "): #, highlight_y):
    """ Draw a menu
    """
    x = 2
    y = 2
    i = 0
    menu_win["win"].box(0, 0)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #curses.init_pair(3, curses.A_UNDERLINE, curses.COLOR_BLACK)

    for widget in menu_win["widgets"]:
        if menu_h and h_ == i + 1:
            menu_win["win"].attron(curses.color_pair(2))
            if menu_win["widgets"][i]["type"] == "label":
                ad_str(menu_win["win"], y + i, x, _cursor + menu_win["widgets"][i]["text"] + "  ", curses.A_UNDERLINE)
            else:
                ad_str(menu_win["win"], y + i, x, _cursor + menu_win["widgets"][i]["text"] + " ")
            menu_win["win"].attroff(curses.color_pair(2))
        else:
            if menu_win["widgets"][i]["type"] == "label":
                #menu_win["win"].attron(curses.color_pair(3))
                ad_str(menu_win["win"], y + i, x, "   " + menu_win["widgets"][i]["text"]+"   ", curses.A_UNDERLINE)
                #menu_win["win"].attroff(curses.color_pair(3))
            else:
                ad_str(menu_win["win"], y + i, x, "- " + menu_win["widgets"][i]["text"] + " ")
        i = i + 1

    menu_win["win"].refresh()


def read(elem, t_name = "Text Input     ", txt = ""):
    elem.timeout(100)
    y, x = elem.getyx()
    text = txt
    orig = txt
    win = curses.newwin(5, 44, 1, 2)
    win.box(0, 0)
    ad_str(win, 1, 1, t_name, curses.A_UNDERLINE)
    ad_str(win, 2, 1, text, curses.A_DIM)
    while True:
        char = elem.getch()
        if char == ord("\n"):
            break
        elif char == curses.KEY_BACKSPACE:
            text = text[0:-1]
            win.clear()
            win.box(0, 0)
            ad_str(win, 1, 1, t_name, curses.A_UNDERLINE)
            #win.refresh()
        elif char == 27 :
            #elem.nodelay(True)
            n = elem.getch()
            if n == -1:
            # Escape was pressed
                elem.timeout(REFRESH_RATE)
                elem.clear()
                return orig
            #elem.nodelay(False)
        else:
            try:
                text += chr(char)
            except:
                pass
        ad_str(win, 2, 1, text + "_")
        #elem.refresh()
        win.refresh()
    elem.timeout(REFRESH_RATE)
    elem.clear()
    return text

def ad_str(element, y, x, str, style = None ):
    try:
        if style != None:
            element.addstr(y, x, str, style)
        else:
            element.addstr(y, x, str)
    except:
        #print("the screen is likely too small")
        element.addstr(0, 0, "the screen is likely too small")