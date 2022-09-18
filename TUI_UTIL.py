
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
        self.elem.hline(0, 0, curses.ACS_CKBOARD, x)
        ad_str(self.elem, 0, 0, self.stat, curses.A_STANDOUT)

def print_button(win, text, y, x, state = True, cursor = " - ", maxL = 15):
    # state cloud be disabled fo buttons
    cl = len(cursor)
    win.attron(curses.color_pair(2))
    ad_str(win, y, x, cursor)
    win.attroff(curses.color_pair(2))
    ad_str(win, y, x + cl, text, curses.A_BOLD)
    return 0 + cl# specific offset for next element
def print_label(win, text, y, x, state = True, cursor = "   ", maxL = 15):
    # nothing for state, its a frkn label
    cl = len(cursor)
    win.attron(curses.color_pair(2))
    ad_str(win, y, x, cursor)
    win.attroff(curses.color_pair(2))
    ad_str(win, y, x + cl, " " + text + " ", curses.A_UNDERLINE)
    return 2 + cl # specific offset for next element
def print_checkbox(win, text, y, x, state = True, cursor = "   ", maxL = 15):
    cl = len(cursor)
    win.attron(curses.color_pair(2))
    ad_str(win, y, x, cursor)
    win.attroff(curses.color_pair(2))
    if state: ad_str(win, y, x + cl, "×") else: ad_str(win, y, x + cl, "¤")
    ad_str(win, y, x + cl + 1, " " + text)
    return 1 + cl # specific offset for next element
def print_slider(win, text, y, x, state = 0, cursor = "", maxL = 15, vertical = False):
    #cl = len(cursor)
    y, x = win.getmaxyx()
    win.attron(curses.color_pair(2))
    #ad_str(win, y, x, cursor)
    win.attroff(curses.color_pair(2))
    #if state: ad_str(win, y, x + cl, "×") else: ad_str(win, y, x + cl, "¤")
    ad_str(win, y, x, "[" + text + "]")
    return 2 + cl # specific offset for next element

def print_menu(menu_win, h_, menu_h, _cursor = "   ", _clean = False): #, highlight_y):
    x = 1
    y = 1
    i = 0
    offset = 0
    clean = False
    max_y, max_x = menu_win["win"].getmaxyx()
    
    if _clean :
        menu_win["win"].clear()
    menu_win["win"].box(0, 0)
    if "name" in menu_win:
        ad_str(menu_win["win"], 0, 1, menu_win["name"], curses.A_REVERSE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #curses.init_pair(3, curses.A_UNDERLINE, curses.COLOR_BLACK)

    # for horizontal placement
    #  + i * (width/len(menu_win["widgets"]))
    # HORIZONTAL MENU
    if menu_win["type"] == "horizontal":
        aux = (int)(max_x/len(menu_win["widgets"]))

        for widget in menu_win["widgets"]:
        
            if menu_h and h_ == i + 1:
                menu_win["win"].attron(curses.color_pair(2))
                ### put widget diferentiation in different function ###
                if menu_win["widgets"][i]["type"] == "label":
                    clean = True
                    ad_str(menu_win["win"], y, x + offset, _cursor + menu_win["widgets"][i]["text"] + " ", curses.A_UNDERLINE)
                    offset += 1
                else:
                    ad_str(menu_win["win"], y, x + offset, _cursor + menu_win["widgets"][i]["text"] + " ")
                menu_win["win"].attroff(curses.color_pair(2))
                offset += 1
            else:
                if menu_win["widgets"][i]["type"] == "label":
                    #aux = (int)(max_x/len(menu_win["widgets"]))
                    aux2 = len(menu_win["widgets"][i]["text"])
                    if aux2 > aux :
                        ad_str(menu_win["win"], y, x + offset, " " + menu_win["widgets"][i]["text"][0:aux] + "..", curses.A_UNDERLINE)
                        offset = offset - aux2 + aux + 1
                        #clean = True
                    else:
                        clean = True
                        ad_str(menu_win["win"], y, x + offset, " " + menu_win["widgets"][i]["text"] + " ", curses.A_UNDERLINE)
                    
                    #ad_str(menu_win["win"], y, x + offset," " + menu_win["widgets"][i]["text"] + " ", curses.A_UNDERLINE)
                    menu_win["win"].addstr(" ") # ugly but still the most efficient fix
                    #menu_win["win"].attroff(curses.color_pair(3))
                else:
                    ad_str(menu_win["win"], y, x + offset, "- " + menu_win["widgets"][i]["text"] + " ")

            offset = offset + len(menu_win["widgets"][i]["text"]) + 3
            i = i + 1
        menu_win["win"].refresh()
        return clean # you can use an XOR here.. I think

    # VERTICAL MENU
    for widget in menu_win["widgets"]:
        
        if menu_h and h_ == i + 1:
            menu_win["win"].attron(curses.color_pair(2))
            ### put widget diferentiation in different function ###
            if menu_win["widgets"][i]["type"] == "label":
                ad_str(menu_win["win"], y + offset, x, _cursor + menu_win["widgets"][i]["text"], curses.A_UNDERLINE)
                aux = len(menu_win["widgets"][i]["text"]) / (max_x)
                if aux > 1 :
                    clean = True
                    offset = offset + (int)(aux)
            else:
                ad_str(menu_win["win"], y + offset, x, _cursor + menu_win["widgets"][i]["text"] + " ")
            menu_win["win"].attroff(curses.color_pair(2))
        else:
            if menu_win["widgets"][i]["type"] == "label":
                #menu_win["win"].attron(curses.color_pair(3))
                aux = len(menu_win["widgets"][i]["text"]) + 8 - max_x
                if aux <= 0 :
                    ad_str(menu_win["win"], y + offset, x, menu_win["widgets"][i]["text"], curses.A_UNDERLINE)
                else:
                    ad_str(menu_win["win"], y + offset, x, menu_win["widgets"][i]["text"][0:-aux] + "..", curses.A_UNDERLINE)
                    
                #menu_win["win"].attroff(curses.color_pair(3))
            else:
                ad_str(menu_win["win"], y + offset, x, "- " + menu_win["widgets"][i]["text"] + " ")
        
        
        offset = offset + 1
        i = i + 1

    menu_win["win"].refresh()
    return clean

def clean_win(win):
    my, mx = win.getmaxyx()

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
                #elem.clear()
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
    #elem.clear()
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
