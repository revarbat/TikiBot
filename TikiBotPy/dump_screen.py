try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton
from feeds import SupplyFeed


class DumpScreen(Frame):
    def __init__(self, master):
        super(DumpScreen, self).__init__(master)
        self.master = master
        self.lbl = Label(self, text="Dumping all feeds")
        self.backbtn = RectButton(self, text="Stop", command=self.handle_button_back)
        self.lbl.pack(side=TOP, fill=BOTH, expand=1)
        self.backbtn.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        for feed in SupplyFeed.getAll():
            feed.startFeed()

    def handle_button_back(self):
        for feed in SupplyFeed.getAll():
            feed.stopFeed()
        self.master.screen_pop()

