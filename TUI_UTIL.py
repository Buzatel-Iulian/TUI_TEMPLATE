
import curses
import sys
import traceback
from threading import Thread
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
        ad_hline(self.elem, 0, 0, curses.ACS_HLINE, x)
        ad_str(self.elem, 0, 0, self.stat+" ")

class Tui:
    def __init__(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.STATUS = Status(self.screen, "Use arrow keys to go up and down, Press enter to interact")
        self.win = []
        self.sel = 0
        self.prev_sel = 0
        self.running = False
        self.thr = Thread(target = curses.wrapper, args = (self.handler, ))
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

        while self.running:
            max_y, max_x = stdscr.getmaxyx()

            if prev_max_x != max_x or prev_max_y != max_y :
                self.screen.clear()
                for i in self.win:
                    i.reset(stdscr)
                    #i.show()
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
            elif char == curses.KEY_LEFT:
                self.win[self.sel].key_left()
            elif char == curses.KEY_RIGHT:
                self.win[self.sel].key_right()
            elif char == ord("\n"):  # Enter
                self.win[self.sel].function()
                self.STATUS.show()
            elif char == 27 :
                self.screen.nodelay(True)
                n = self.screen.getch()
                if n == -1:
                    # Escape was pressed
                    self.screen.nodelay(False)
                    self.running = False
                    break
                self.screen.nodelay(False)
            elif char != -1:
                for i in range(len(self.win)):
                    if self.win[i].key == chr(char):
                        self.prev_sel = self.sel
                        self.sel = i
            
            for i in range(len(self.win)):
                #if i == self.sel or i == self.prev_sel:
                self.win[i].show(i==self.sel)

            ad_hline(self.screen, max_y-1, 0, curses.ACS_HLINE, max_x)
            ad_str(self.screen, max_y-1, 0, " y/H={} x/W={} frame={} ".format(max_y, max_x, count))
            count += 1
            self.screen.refresh()

        #curses.endwin() wrapper does this automatically https://stackoverflow.com/questions/48526043/python-curses-unsets-onlcr-and-breaks-my-terminal-how-to-reset-properly
        #sys.exit(0)  Not sure why I had this
    def start(self):
        self.running = True
        # add try block with endwin to handle sudden program fault not reseting console settings
        try:
            #curses.wrapper(self.handler)
            self.thr.start()
            #self.thr.join()
        except:
            curses.endwin()
            print(traceback.format_exc())
    def stop(self):
        #self.thr.terminate()
        self.running = False
        self.thr.join()
        #curses.endwin()

class Menu:
    def __init__(self, h, w, x, y, key, title = "", scaling = False):
        self.scaling = scaling
        self.HEIGHT = h
        self.WIDTH = w
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.x_ = x
        self.y_ = y
        self.title = title
        #if self.scaling:
        #    max_y, max_x = stdscr.getmaxyx()
        #    self.win = curses.newwin(sc(self.HEIGHT, max_y), sc(self.WIDTH, max_x), sc(self.y, max_y), sc(self.x, max_x))
        #else:
        self.win = curses.newwin(self.HEIGHT, self.WIDTH, self.y, self.x)
        self.widgets = []
        self.key = key
        self.arrow = 0
        self.index = 0
    def add(self, button):
        button.elem = self.win
        self.widgets.append(button)
    def show(self, current):
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        self.win.box(0, 0)
        clean(self.win)
        if current:
            self.win.attron(curses.color_pair(2))
            ad_str(self.win, 0, 1, " "+self.key+":"+self.title+" ")
            self.win.attroff(curses.color_pair(2))
        else:
            ad_str(self.win, 0, 1, " "+self.key+":"+self.title+" ")

        if (len(self.widgets)-1) > (self.HEIGHT - 3):
            aux = self.index + self.HEIGHT - 3
            ad_str(self.win, 1, 1, "["+str(self.index+1)+"-"+str(aux)+"/"+str(len(self.widgets))+"]")
        #for b in range(len(self.widgets)):
            i = 0
            for b in range(self.index, aux):
                self.widgets[b].show(i+2, b==self.arrow and current)
                i += 1
        else:
            for b in range(len(self.widgets)):
                self.widgets[b].show(b+2, b==self.arrow and current)
        self.win.refresh()
    def function(self):
        self.widgets[self.arrow].function()
    def fit(self):
        aux = len(self.widgets)-1
        if self.arrow > aux:
            self.arrow = 0
            self.index = 0
            return
        if self.arrow < 0:
            self.arrow = aux
            self.index = aux - (self.HEIGHT - 4)
            return
        if self.arrow < self.index:
            self.index -= 1
        if self.arrow >= (self.index + self.HEIGHT - 3):
            self.index += 1
    def key_up(self):
        self.arrow -=1
        while not(self.widgets[self.arrow].active):
            self.arrow -=1
            self.fit()
        self.fit()
        #if self.arrow < self.index:
        #    self.index -= 1
    def key_down(self):
        self.arrow +=1
        self.fit()
        while not(self.widgets[self.arrow].active):
            self.arrow +=1
            self.fit()
        self.fit()
        #if self.arrow >= (self.index + self.HEIGHT - 3):
        #    self.index += 1
    def key_left(self):
        self.widgets[self.arrow].key_left()
    def key_right(self):
        self.widgets[self.arrow].key_right()
    def reset(self, stdscr_):
        if self.scaling:
            max_y, max_x = stdscr_.getmaxyx()
            self.HEIGHT = sc(self.h, max_y)
            self.WIDTH = sc(self.w, max_x)
            self.x = sc(self.x_, max_x)
            self.y = sc(self.y_, max_y)
        else:
            self.HEIGHT = self.h
            self.WIDTH = self.w
            self.x = self.x_
            self.y = self.y_
        self.win = curses.newwin(self.HEIGHT, self.WIDTH, self.y, self.x)
        for b in self.widgets:
            b.elem = self.win
            b.reset(stdscr_)

class Widget:
    def __init__(self):
        return
    def function(self):
        return
    def show(self):
        return
    def reset(self):
        return
    def key_left(self):
        return
    def key_right(self):
        return

class Button(Widget):
    def __init__(self, text, func):
        self.active = True
        self.elem = None
        self.text = text
        self.func = func
        self.crop = 3
    def function(self):
        self.func()
    def show(self, x, sel):
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        if sel:
            self.elem.attron(curses.color_pair(2))
            ad_str(self.elem, x, 2, cr(self.text, self.crop))
            self.elem.attroff(curses.color_pair(2))
            return
        ad_str(self.elem, x, 2, cr(self.text, self.crop))
        #self.elem.refresh()
    def reset(self, stdscr_):
        aux, self.crop = self.elem.getmaxyx()
        self.crop -= 3

class Toggle(Widget):
    def __init__(self, text, func = None):
        self.active = True
        self.elem = None
        self.text = text
        self.func = func
        self.onoff = False
        self.crop = 3
    def function(self):
        if self.func != None:
            self.func()
        self.onoff = not(self.onoff)
    def show(self, x, sel):
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        if sel:
            self.elem.attron(curses.color_pair(2))
            ad_str(self.elem, x, 1, ("+" if self.onoff else "-") + cr(self.text, self.crop))
            self.elem.attroff(curses.color_pair(2))
            return
        ad_str(self.elem, x, 1, ("+" if self.onoff else "-") + cr(self.text, self.crop))
        #self.elem.refresh()
    def reset(self, stdscr_):
        aux, self.crop = self.elem.getmaxyx()
        self.crop -= 3

class Label(Widget):
    def __init__(self, text = ""):
        self.active = False
        self.elem = None
        self.stdscr = None
        self.text = text
        self.crop = 3
    def function(self):
        return
    def reset(self, stdscr_):
        self.stdscr = stdscr_
        aux, self.crop = self.elem.getmaxyx()
        self.crop -= 3
    def show(self, x, sel):
        ad_str(self.elem, x, 1, cr(self.text, self.crop), curses.A_UNDERLINE)

class Text(Widget):
    def __init__(self, text = ""):
        self.active = True
        self.elem = None
        self.stdscr = None
        self.text = text
        self.crop = 3
    def function(self):
        self.text = read(self.stdscr, "Text Field", self.text)
    def reset(self, stdscr_):
        self.stdscr = stdscr_
        aux, self.crop = self.elem.getmaxyx()
        self.crop -= 3
    def show(self, x, sel):
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
        if sel:
            aux,l = self.elem.getmaxyx()
            #ad_hline(self.elem, x, 1, " ", l-2)
            self.elem.attron(curses.color_pair(3))
            ad_str(self.elem, x, 2, cr(self.text, self.crop))
            self.elem.attroff(curses.color_pair(3))
            return
        ad_str(self.elem, x, 2, cr(self.text, self.crop), curses.A_REVERSE)

class Numeric(Widget):
    def __init__(self, text = "", value = 0, min_ = 0, max_ = 100):
        self.active = True
        self.increment = True
        self.elem = None
        self.stdscr = None
        self.text = text
        self.value = value
        self.min_ = min_
        self.max_ = max_
        self.crop = 3
    def function(self):
        return
    def reset(self, stdscr_):
        self.stdscr = stdscr_
        aux, self.crop = self.elem.getmaxyx()
        self.crop -= 3
    def show(self, x, sel):
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        if sel:
            aux,l = self.elem.getmaxyx()
            #ad_hline(self.elem, x, 1, " ", l-2)
            self.elem.attron(curses.color_pair(2))
            ad_str(self.elem, x, 2, cr("<" + str(self.value) + "> " + self.text, self.crop))
            self.elem.attroff(curses.color_pair(2))
            return
        ad_str(self.elem, x, 2, cr("<" + str(self.value) + "> " + self.text, self.crop))
    def key_left(self):
        self.value -= 1
        if self.value < self.min_:
            self.value = self.min_
    def key_right(self):
        self.value += 1
        if self.value > self.max_:
            self.value = self.max_



def sc(v_in, v_dim):
    return int(v_dim*(v_in/100))

def cr(str_in, cr_dim):
    if len(str_in) > cr_dim:
        return str_in[0:(cr_dim-2)]+".."
    return str_in

def read(elem, t_name = "Text Input     ", txt = ""):
    elem.timeout(100)
    max_y, max_x = elem.getmaxyx()
    text = txt
    orig = txt
    win = curses.newwin(sc(30, max_y), sc(80, max_x), sc(35, max_y), sc(10, max_x))
    win.box(0, 0)
    ad_str(win, 1, 1, t_name, curses.A_UNDERLINE)
    ad_str(win, 2, 1, text, curses.A_DIM)
    while True:
        p_y, p_x = max_y, max_x
        max_y, max_x = elem.getmaxyx()
        if max_y != p_y or max_x != p_x:
            elem.clear()
            win = curses.newwin(sc(30, max_y), sc(80, max_x), sc(35, max_y), sc(10, max_x))
            win.box(0, 0)
            ad_str(win, 1, 1, t_name, curses.A_UNDERLINE)
            elem.refresh()
            text = text[0:-1]
            continue
        char = elem.getch()
        if char == ord("\n"):
            break
        elif char == curses.KEY_BACKSPACE:
            text = text[0:-1]
            #win.clear()
            clean(win)
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

def clean(element):
    max_y, max_x = element.getmaxyx()
    for i in range(max_y-2):
        ad_hline(element, i+1, 1, " ", max_x-2)


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
