try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import math
import operator
from feeds import SupplyFeed
from recipes import Recipe
from select_screen import SelectScreen
from alpha_screen import AlphaScreen
from feed_edit_screen import FeedEditScreen
from list_screen import ListScreen
from notify_screen import NotifyScreen


class ManageFeedsScreen(ListScreen):
    def __init__(self, master):
        super(ManageFeedsScreen, self).__init__(
            master,
            self._get_items,
            label_text="Select a feed to manage:",
            add_cb=self.item_add,
            del_cb=self.item_del,
            edit_cb=self.item_edit,
            raise_cb=self.item_raise,
            lower_cb=self.item_lower,
        )

    def _get_items(self):
        return [
            {
                "name": "#%d %s" % (feed.motor_num, feed.getName()),
                "data": feed,
                "fgcolor": None if feed.avail else "#700",
            }
            for feed in SupplyFeed.getAllOrdered()
        ]

    def activate(self):
        self.update_listbox()

    def item_add(self):
        try:
            for n in range(99):
                name = "Feed %d" % (n+1)
                SupplyFeed.getByName(name)
        except KeyError:
            pass
        self.master.screen_push(AlphaScreen(self.master, label="Name for New Feed:", defval=name, callback=self._item_add_finish))

    def _item_add_finish(self, name):
        flowrate = 14.2
        overage = 0.25
        for lastfeed in SupplyFeed.getAllOrdered():
            flowrate = lastfeed.flowrate
            overage = lastfeed.pulse_overage
        feed = SupplyFeed("Misc", name, flowrate=flowrate, overage=overage)
        self.master.save_configs()
        self.update_listbox()
        self.master.screen_pop()
        self.master.screen_push(FeedEditScreen(self.master, feed))

    def item_del(self, idx, txt, feed):
        self.sel_feed = feed
        recipes = Recipe.getRecipesByFeed(feed)
        if recipes:
            self.master.screen_push(NotifyScreen(self.master, text="That feed is currently in use by one or more recipes."))
        else:
            self.master.screen_push(SelectScreen(self.master, ["Confirm"], labeltext='Delete feed "%s"?' % txt, callback=self._item_del_finish))

    def _item_del_finish(self, confirm):
        if confirm == "Confirm":
            self.sel_feed.delete_feed()
            self.master.save_configs()
        self.master.screen_pop()

    def item_edit(self, idx, txt, feed):
        self.master.screen_push(FeedEditScreen(self.master, feed))

    def item_raise(self, idx, txt, feed):
        SupplyFeed.transpose(idx-1)
        self.master.save_configs()

    def item_lower(self, idx, txt, feed):
        SupplyFeed.transpose(idx)
        self.master.save_configs()


