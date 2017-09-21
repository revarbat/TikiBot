try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import os
import sys
from rectbutton import RectButton


class ShutdownScreen(Frame):
    def __init__(self, master):
        super(ShutdownScreen, self).__init__(master)
        quitbtn = RectButton(self, text="Quit Tikibot", command=self.handle_button_quit)
        bootbtn = RectButton(self, text="Reboot System", command=self.handle_button_restart)
        offbtn = RectButton(self, text="Shutdown System", command=self.handle_button_off)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)
        quitbtn.grid(column=1, row=1, pady=10, sticky=N+E+W)
        bootbtn.grid(column=1, row=2, pady=20, sticky=N+E+W)
        offbtn.grid(column=1, row=3, pady=10, sticky=N+E+W)
        backbtn.grid(column=1, row=9, pady=10, sticky=S+E)
        self.columnconfigure(0, weight=1, minsize=20)
        self.columnconfigure(3, minsize=20)
        self.rowconfigure(0, minsize=10)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, minsize=10)

    def handle_button_quit(self):
        sys.exit(0)

    def handle_button_off(self):
        os.system("sudo poweroff")

    def handle_button_restart(self):
        os.system("sudo reboot")

    def handle_button_back(self):
        self.master.screen_pop()


