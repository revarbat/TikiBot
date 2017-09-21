try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import math
import operator
from feeds import SupplyFeed
from select_screen import SelectScreen
from feed_screen import FeedScreen


class ManageFeedsScreen(SelectScreen):
    def __init__(self, master):
        self.master = master
        self.cols = 3
        button_configs = self._calc_buttons()
        super(ManageFeedsScreen, self).__init__(master, button_configs, labeltext="Select a feed to manage:", cols=self.cols)

    def _calc_buttons(self):
        feeds = SupplyFeed.getAll()
        button_configs = [
            {
                "name": "#%d %s" % (feed.motor_num, feed.getName()),
                "fgcolor": None if feed.avail else "#700",
                "icon": None if feed.avail else "Disabled.gif",
                "compound": LEFT,
            }
            for feed in sorted(feeds, key=operator.attrgetter('motor_num'))
        ]
        self.cols = max(2, math.ceil(len(button_configs)/7))
        return button_configs

    def activate(self):
        button_configs = self._calc_buttons()
        self.update_buttons(button_configs, self.cols)

    def handle_button_select(self, item):
        name = item.split(" ", 1)[1]
        feed = SupplyFeed.getByName(name)
        self.master.screen_push(FeedScreen(self.master, feed))


