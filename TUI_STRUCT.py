import curses
import sys
from TUI_UTIL import *

class Structure:
    def __init__(self, screen):
        self.screen = screen
        self.interface = {}
        self.fast_keys = {}
        self.command_keys = {}
        self.displays = {}
        self.start()


    def start(self):
        y,x = self.screen.getmaxyx()
        self.fast_keys = {'1':0, '2':1}
        self.command_keys = {}
        self.displays = {}
        self.interface =  [
            {
                "name":"MODS",
                #"win":curses.newwin(HEIGHT, WIDTH, 1, 2),
                "win":curses.newwin(10, 22, 1, 2),
                "widgets":[
                    {"text":"TESSELATION","type":"checkbox"},
                    {"text":"CONTOURS","type":"checkbox"},
                    {"text":"MARKS","type":"checkbox"},
                    {"text":"IRISES","type":"checkbox"},
                ]
            },
            {
                "name":"USED MODEL",
                "win":curses.newwin(y - 2, 22, 1, 25),
                "widgets":[
                    {"text":"LOAD","type":"button"},
                    {"text":"LOADED MODEL","type":"label"},
                    {"text":"MASK_ON","type":"checkbox"},
                ]
            }
        ]