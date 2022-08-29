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

    def refresh(self):
        y,x = self.screen.getmaxyx()
        self.interface = self.interface
        self.fast_keys = self.fast_keys
        self.command_keys = self.command_keys
        self.displays = self.displays

    def start(self):
        y,x = self.screen.getmaxyx()
        self.fast_keys = {'1':0, '2':1}
        self.command_keys = {}
        self.displays = {}
        self.interface =  [
            {
                "name":"MODS",
                "type":"vertical",
                #"win":curses.newwin(HEIGHT, WIDTH, 1, 2),
                "win":curses.newwin(10, 22, 4, 2),
                "widgets":[
                    {"text":"TESSELATION","type":"checkbox"},
                    {"text":"CONTOURS","type":"checkbox"},
                    {"text":"MARKS","type":"checkbox"},
                    {"text":"IRISES","type":"checkbox"},
                ]
            },
            {
                "name":"USED MODEL",
                "type":"vertical",
                "win":curses.newwin(y - 5, 22, 4, 25),
                "widgets":[
                    {"text":"LOAD","type":"button"},
                    {"text":"LOADED MODEL⠗⠗hhhhhhhhhhhhhhhhhhhh⠗⠗hh","type":"text"},
                    {"text":"MASK_ON","type":"checkbox"},
                ]
            },
            {
                #"name":"USED MODEL",
                "type":"horizontal",
                "win":curses.newwin(3, x - 4, 1, 2),
                "widgets":[
                    {"text":"LOAD","type":"button"},
                    {"text":"LOAD_again","type":"button"},
                    {"text":"LOADED MODELllllllllllllllllllllllllllllllllll","type":"text"},
                    {"text":"MASK_ON","type":"checkbox"},
                ]
            }
        ]