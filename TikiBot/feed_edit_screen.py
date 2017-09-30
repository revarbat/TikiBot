try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton
from alpha_screen import AlphaScreen
from select_screen import SelectScreen
from calib_screen import CalibScreen
from touch_checkbox import TouchCheckbox
from touch_spinner import TouchSpinner


class FeedEditScreen(Frame):
    def __init__(self, master, feed):
        super(FeedEditScreen, self).__init__(master)
        self.master = master
        self.feed = feed
        self.avail = IntVar()
        self.avail.set(1 if feed.avail else 0)

        self.lbl = Label(self, text="Feed #%d: %s" % (feed.motor_num, feed.getName()))
        renamebtn = RectButton(self, text="Rename Feed", width=150, command=self.handle_button_rename)
        calibbtn = RectButton(self, text="Calibration", width=150, command=self.handle_button_calib)
        self.feedbtn = RectButton(self, text="Start Feed", width=150, command=self.handle_button_feed)
        enbtn = TouchCheckbox(self, text="Available", variable=self.avail, command=self.handle_button_enable)
        self.proofspin = TouchSpinner(self, width=150, value=self.feed.proof, minval=0, maxval=200, incdecval=1, format="Proof: %d", changecmd=self.handle_proof_change)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)

        self.lbl.grid(column=1, row=1, columnspan=2, pady=20, sticky=E+W)
        renamebtn.grid(column=1, row=2, padx=20, pady=10, sticky=E+W)
        calibbtn.grid(column=1, row=3, padx=20, pady=10, sticky=E+W)
        self.feedbtn.grid(column=1, row=4, padx=20, pady=10, sticky=E+W)
        enbtn.grid(column=2, row=2, padx=20, pady=10, sticky=E+W)
        self.proofspin.grid(column=2, row=3, rowspan=3, padx=20, pady=10)
        backbtn.grid(column=2, row=9, columnspan=3, padx=20, pady=10, sticky=S+E)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, minsize=10)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(10, minsize=10)

    def handle_proof_change(self, oldval, newval):
        self.feed.proof = newval

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


