try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import math
import operator
from feeds import SupplyFeed
from select_screen import SelectScreen
from alpha_screen import AlphaScreen
from feed_edit_screen import FeedEditScreen


class ManageFeedsScreen(SelectScreen):
    def __init__(self, master):
        self.master = master
        self.cols = 3
        button_configs = self._calc_buttons()
        super(ManageFeedsScreen, self).__init__(master, button_configs, labeltext="Select a feed to manage:", cols=self.cols)

    def _calc_buttons(self):
        button_configs = [
            {
                "name": "#%d %s" % (feed.motor_num, feed.getName()),
                "fgcolor": None if feed.avail else "#700",
                "icon": None if feed.avail else "Disabled.gif",
                "compound": LEFT,
                "callback": lambda x=feed: self.handle_button_select(x),
            }
            for feed in SupplyFeed.getAllOrdered()
        ]
        self.cols = max(2, math.ceil(len(button_configs)/7))
        return button_configs

    def activate(self):
        button_configs = self._calc_buttons()
        self.update_buttons(button_configs, self.cols)

    def handle_button_select(self, feed):
        self.master.screen_push(FeedEditScreen(self.master, feed))

    def handle_button_new(self):
        try:
            for n in range(99):
                name = "Feed %d" % (n+1)
                SupplyFeed.getByName(name)
        except KeyError:
            pass
        self.master.screen_push(AlphaScreen(self.master, label="Name for New Feed:", defval=name, callback=self._new_feed_finish))

    def _new_feed_finish(self, name):
        flowrate = 14.2
        overage = 0.25
        for lastfeed in SupplyFeed.getAllOrdered():
            flowrate = lastfeed.flowrate
            overage = lastfeed.pulse_overage
        feed = SupplyFeed("Misc", name, flowrate=flowrate, overage=overage)
        self.master.screen_pop()
        self.master.screen_push(FeedEditScreen(self.master, feed))


