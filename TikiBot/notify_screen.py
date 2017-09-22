try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton


class NotifyScreen(Frame):
    def __init__(self, master, text=""):
        super(NotifyScreen, self).__init__(master)
        self.master = master
        lbl = Label(self, text=text, font="Helvetica 24")
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)
        lbl.grid(column=1, row=1, sticky=E+W)
        backbtn.grid(column=1, row=3, sticky=S+E)
        self.grid_columnconfigure(0, minsize=10)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(9, minsize=10)
        self.grid_rowconfigure(0, minsize=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(9, minsize=10)

    def handle_button_back(self):
        self.master.screen_pop()

