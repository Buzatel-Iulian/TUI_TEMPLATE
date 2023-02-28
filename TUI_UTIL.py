
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

class Tui:
    def __init__(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.STATUS = Status(self.screen, "Use arrow keys to go up and down, Press enter to select a choice")
        self.win = []
        self.sel = 0
        self.prev_sel = 0
    def addMenu(self, menu):
        self.win.append(menu)
    def handler(self, stdscr):
        count = 0
        prev_max_x = 0
        prev_max_y = 0
        curses.noecho()
        curses.curs_set(0)
        self.screen.scrollok(True)
        self.screen.keypad(True)
        self.screen.timeout(REFRESH_RATE)
        curses.cbreak()  # Line buffering disabled. pass on everything
        self.screen.refresh()

        while True:
            max_y, max_x = stdscr.getmaxyx()

            if prev_max_x != max_x or prev_max_y != max_y :
                self.screen.clear()
                self.STATUS.show()
            prev_max_x = max_x
            prev_max_y = max_y

            try:
                char = self.screen.getch()
            except:
                pass

            if char == curses.KEY_UP:
                self.win[self.sel].key_up()
            elif char == curses.KEY_DOWN:
                self.win[self.sel].key_down()
            elif char == ord("\n"):  # Enter
                self.win[self.sel].function()
            elif char == 27 :
                self.screen.nodelay(True)
                n = self.screen.getch()
                if n == -1:
                    # Escape was pressed
                    self.screen.nodelay(False)
                    break
                self.screen.nodelay(False)
            elif char != -1:
                for i in range(len(self.win)):
                    if self.win[i].key == char:
                        self.prev_sel = self.sel
                        self.sel = i
            
            for i in range(len(self.win)):
                if i == self.sel or i == self.prev_sel:
                    self.win[i].show()

            ad_hline(self.screen, max_y-1, 0, curses.ACS_HLINE, max_x)
            ad_str(self.screen, max_y-1, 0, " y/H={} x/W={} frame={} ".format(max_y, max_x, count))
            count += 1
            self.screen.refresh()

        curses.endwin()
        sys.exit(0)
    def start(self):
        curses.wrapper(self.handler)



class Menu:
    def __init__(self, elem, HEIGHT, WIDTH, x, y, key):
        self.win = curses.newwin(HEIGHT, WIDTH, y, x)
        self.elem = elem
        self.widgets = []
        self.key = key
        self.arrow = 0
    def addButton(self, button):
        self.widgets.append(button)
    def show(self):
        self.win.box(0, 0)
        ad_str(self.win, 0, 1, key, curses.A_REVERSE)
        i=2
        for b in self.widgets:
            b.show(i, i==slef.arrow-2)
            i += 1
    def function(self):
        widgets[self.arrow].function()
    def key_up(self):
        self.arrow +=1
    def key_down(self):
        self.arrow -=1

class Button:
    def __init__(self, elem, text, func, toggle = False):
        self.elem = elem
        self.text = text
        self.func = func
        self.toggle = toggle
        self.onoff = False
    def function(self):
        self.func()
        self.onoff = not(self.onoff)
    def show(self, x, sel):
        ad_str(self.elem, x, 2, self.text + (" +" if self.onoff else " -") if toggle else "", curses.A_UNDERLINE if sel else curses.A_DIM)

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
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
        element.attron(curses.color_pair(3))
        element.addstr(1, 0, "<overflow>")
        element.attroff(curses.color_pair(3))

def ad_hline(element, y, x, Mrk, l):
    try:
        element.hline(y, x, Mrk, l)
    except:
        #print("the screen is likely too small")
        element.addstr(0, 0, "the screen is likely too small")
