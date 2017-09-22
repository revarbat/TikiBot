#!/usr/bin/env python3

try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import os
import sys
import yaml
import platform
from pkg_resources import resource_string

from feeds import SupplyFeed
from recipes import Recipe
from main_screen import MainScreen


class TikiBotGui(Tk):
    def __init__(self):
        super(TikiBotGui, self).__init__()
        self.passcode = "8888"
        self.screen_stack = []
        self.image_cache = {}
        self.title("TikiBot")
        if platform.system() == "Linux":
            self.attributes("-fullscreen", True)
            self.protocol("WM_DELETE_WINDOW", lambda: false)
            self.option_add("*cursor", "none")
            self.option_add("*font", "Helvetica 16")
            self.option_add("*Text*font", "Helvetica 20")
            self.option_add("*Pour*Button*font", "Helvetica 20")
            self.option_add("*TouchSpinner*font", "Helvetica 16")
            self.option_add("*Amount*TouchSpinner*Label*font", "Helvetica 24")
            self.option_add("*Button*background", "#ccc")
            self.option_add("*Button*activeBackground", "#ccc")
        else:
            self.geometry("800x480")
            self.option_add("*font", "Helvetica 16")
            self.option_add("*Text*font", "Helvetica 20")
            self.option_add("*Pour*Button*font", "Helvetica 20")
            self.option_add("*Amount*TouchSpinner*Label*font", "Helvetica 24")
            self.option_add("*Button*background", "#ccc")
            self.option_add("*Button*activeBackground", "#ccc")
        self.bind('<Key-Escape>', lambda evt: sys.exit(0))
        self.load_configs()
        self.screen_push(MainScreen(self))

    def set_passcode(self, newpass):
        self.passcode = newpass

    def load_configs(self):
        misc_confs = yaml.load(self.get_resource("misc_config.yaml"))
        self.passcode = misc_confs.get('passcode', '8888')
        SupplyFeed.load(self.get_resource("feeds_config.yaml"))
        Recipe.load(self.get_resource("recipes_config.yaml"))

    def save_configs(self):
        misc_confs = {
            "passcode": self.passcode,
        }
        self.set_resource("misc_config.yaml", yaml.dump(misc_confs))
        self.set_resource("feeds_config.yaml", SupplyFeed.dump())
        self.set_resource("recipes_config.yaml", Recipe.dump())

    def set_resource(self, name, data):
        with open(os.path.join("resources", name), "w") as f:
            f.write(data)

    def get_resource(self, name):
        with open(os.path.join("resources", name), "r") as f:
            return f.read()
        return None
        #return resource_string('TikiBotPy.resources', name)

    def get_image(self, imgname):
        if imgname in self.image_cache:
            return self.image_cache[imgname]
        if imgname:
            img = PhotoImage(file=os.path.join("resources", "images", imgname))
            #img = PhotoImage(data=resource_string('TikiBotPy.resources.images', imgname).encode('base64'))
        else:
            img = PhotoImage(width=1, height=1)
        self.image_cache[imgname] = img
        return img

    def screen_push(self, screen):
        if self.screen_stack:
            self.screen_stack[-1].forget()
        self.screen_stack.append(screen)
        screen.pack(side=LEFT, fill=BOTH, expand=1)
        self.after(10, self.update)

    def screen_pop(self):
        if self.screen_stack:
            self.screen_stack.pop().forget()
        if self.screen_stack:
            top = self.screen_stack[-1]
            top.pack(side=LEFT, fill=BOTH, expand=1)
            if callable(getattr(top, "activate", None)):
                top.activate()
        self.after(10, self.update)

    def screen_pop_to_top(self):
        if self.screen_stack:
            self.screen_stack.pop().forget()
        while len(self.screen_stack) > 1:
            self.screen_stack.pop()
        if self.screen_stack:
            self.screen_stack[-1].pack(side=LEFT, fill=BOTH, expand=1)
        self.after(10, self.update)


bot = TikiBotGui()
bot.mainloop()

