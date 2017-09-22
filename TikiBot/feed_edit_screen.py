try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton
from alpha_screen import AlphaScreen
from select_screen import SelectScreen
from calib_screen import CalibScreen


class FeedEditScreen(Frame):
    def __init__(self, master, feed):
        super(FeedEditScreen, self).__init__(master)
        self.master = master
        self.feed = feed
        self.avail = IntVar()
        self.avail.set(1 if feed.avail else 0)

        self.lbl = Label(self, text="Feed #%d: %s" % (feed.motor_num, feed.getName()))
        renamebtn = RectButton(self, text="Rename Feed", width=150, command=self.handle_button_rename)
        orderdnbtn = RectButton(self, text="Incr Motor #", width=150, command=self.handle_button_feed_orderdn)
        orderupbtn = RectButton(self, text="Decr Motor #", width=150, command=self.handle_button_feed_orderup)
        delbtn = RectButton(self, text="Delete Feed", width=150, command=self.handle_button_feed_del)
        enbtn = Checkbutton(self, text="Available", variable=self.avail, command=self.handle_button_enable)
        calibbtn = RectButton(self, text="Calibration", width=150, command=self.handle_button_calib)
        self.feedbtn = RectButton(self, text="Start Feed", width=150, command=self.handle_button_feed)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)

        self.lbl.grid(column=1, row=1, columnspan=2, pady=10, sticky=E+W)
        renamebtn.grid(column=1, row=3, padx=20, pady=10, sticky=E+W)
        orderdnbtn.grid(column=1, row=4, padx=20, pady=10, sticky=E+W)
        orderupbtn.grid(column=1, row=5, padx=20, pady=10, sticky=E+W)
        delbtn.grid(column=1, row=6, padx=20, pady=10, sticky=E+W)

        enbtn.grid(column=2, row=3, padx=20, pady=10)
        calibbtn.grid(column=2, row=4, padx=20, pady=10, sticky=E+W)
        self.feedbtn.grid(column=2, row=5, padx=20, pady=10, sticky=E+W)
        backbtn.grid(column=2, row=9, columnspan=2, padx=20, pady=10, sticky=S+E)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
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

    def handle_button_feed_orderup(self):
        self.feed.reorderUp()
        self.lbl.config(text="Feed #%d: %s" % (self.feed.motor_num, self.feed.getName()))

    def handle_button_feed_orderdn(self):
        self.feed.reorderDown()
        self.lbl.config(text="Feed #%d: %s" % (self.feed.motor_num, self.feed.getName()))

    def handle_button_feed_del(self):
        self.master.screen_push(SelectScreen(self.master, ["Confirm"], labeltext="Are you sure you want to delete this feed?", callback=self.feed_delete_complete))

    def feed_delete_complete(self, confirm):
        if confirm == "Confirm":
            self.feed.delete_feed()
            self.master.save_configs()
            self.master.screen_pop()
        self.master.screen_pop()


