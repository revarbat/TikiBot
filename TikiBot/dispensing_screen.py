try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import time
from rectbutton import RectButton


UPDATE_MS = 20
DISPLAY_MS = 125


class DispensingScreen(Frame):
    def __init__(self, master, recipe, amount):
        super(DispensingScreen, self).__init__(master)
        self.master = master
        self.recipe = recipe
        self.last_disp = 0.0
        self.desc = Text(self, relief=FLAT, wrap=NONE, state=DISABLED)
        backbtn = RectButton(self, text="Cancel", command=self.handle_button_back)

        self.desc.grid(column=0, row=0, sticky=N+E+W+S)
        backbtn.grid(column=0, row=1, padx=10, pady=10, sticky=E+W+S)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        recipe.startDispensing(amount)
        self.pid = self.after(UPDATE_MS, self.update_screen)

    def update_screen(self):
        self.pid = None
        recipe = self.recipe
        recipe.updateDispensing()
        now = time.time() * 1000.0
        if now - self.last_disp >= DISPLAY_MS:
            self.last_disp = now
            self.desc.config(state=NORMAL)
            self.desc.delete(0.0, END)
            self.desc.tag_config("header", background="#077", foreground="white")
            self.desc.tag_config("ingr", lmargin1=10, lmargin2=20)
            self.desc.tag_config("percent", foreground="#c44")
            self.desc.insert(END, "Dispensing: %s\n" % recipe.getName(), "header")
            for ingr in recipe.dispensing:
                self.desc.insert(END, ingr.readableDesc(), "ingr")
                self.desc.insert(END, " ")
                self.desc.insert(END, "%.0f%%\n" % ingr.percentDone(), 'percent')
            self.desc.config(state=DISABLED)
            self.master.update()
        if recipe.doneDispensing():
            self.master.screen_pop_to_top()
        else:
            self.pid = self.after(UPDATE_MS, self.update_screen)

    def handle_button_back(self):
        if self.pid != None:
            self.after_cancel(self.pid)
        self.recipe.cancelDispensing()
        self.master.screen_pop()

