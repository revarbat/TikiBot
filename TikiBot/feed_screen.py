try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton
from alpha_screen import AlphaScreen
from calib_screen import CalibScreen


class FeedScreen(Frame):
    def __init__(self, master, feed):
        super(FeedScreen, self).__init__(master)
        self.master = master
        self.feed = feed
        self.avail = IntVar()
        self.avail.set(1 if feed.avail else 0)

        self.lbl = Label(self, text="Feed #%d: %s" % (feed.motor_num, feed.getName()))
        enbtn = Checkbutton(self, text="Available", variable=self.avail, command=self.handle_button_enable)
        renamebtn = RectButton(self, text="Rename Feed", command=self.handle_button_rename)
        calibbtn = RectButton(self, text="Calibration", width=120, command=self.handle_button_calib)
        self.feedbtn = RectButton(self, text="Start Feed", width=120, command=self.handle_button_feed)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)

        self.lbl.grid(column=1, row=1, pady=10, sticky=N+E+W)
        enbtn.grid(column=1, row=2, pady=10, sticky=N)
        renamebtn.grid(column=1, row=3, pady=10, sticky=N+E+W)
        calibbtn.grid(column=1, row=4, pady=10, sticky=N+E+W)
        self.feedbtn.grid(column=1, row=5, pady=10, sticky=N+E+W)
        backbtn.grid(column=1, row=9, columnspan=2, padx=20, pady=10, sticky=S+E)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, minsize=10)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(10, minsize=10)

    def handle_button_enable(self, ev=None):
        self.feed.avail = True if self.avail.get() != 0 else False

    def handle_button_feed(self):
        if self.feed.isFlowing():
            self.feed.stopFeed()
            self.feedbtn.config(text="Start Feed")
        else:
            self.feed.startFeed()
            self.feedbtn.config(text="Stop Feed")
        self.master.update()

    def handle_button_rename(self):
        self.master.screen_push(AlphaScreen(self.master, label="Name for feed #%d:" % self.feed.motor_num, defval=self.feed.getName(), callback=self.rename_complete))

    def handle_button_calib(self):
        self.master.screen_push(CalibScreen(self.master, self.feed))

    def handle_button_back(self):
        self.feed.avail = True if self.avail.get() != 0 else False
        self.master.save_configs()
        if self.feed.isFlowing():
            self.feed.stopFeed()
        self.master.screen_pop()

    def rename_complete(self, val):
        self.feed.rename(val)
        self.lbl.config(text="Feed #%d: %s" % (self.feed.motor_num, self.feed.getName()))
        self.master.save_configs()
        self.master.screen_pop()


