try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import math
from rectbutton import RectButton


class SelectScreen(Frame):
    def __init__(self, master, items, callback=None, labeltext=None, cols=3):
        super(SelectScreen, self).__init__(master)
        self.master = master
        self.callback = callback if callback else self.handle_button_select
        self.buttons = []
        if labeltext:
            self.grid_rowconfigure(0, minsize=10)
            lbl = Label(self, text=labeltext)
            lbl.grid(column=1, row=1, columnspan=cols*2-1, sticky=N+W)
            self.grid_rowconfigure(2, minsize=10)
        self.update_buttons(items, cols=cols)
        if callable(getattr(self, "handle_button_new", None)):
            newbtn = RectButton(self, text="\u2795", width=40, command=self.handle_button_new)
            newbtn.grid(column=1, row=98, sticky=S+W)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)
        backbtn.grid(column=cols*2-1, row=98, sticky=S+E)
        self.grid_rowconfigure(97, weight=1)
        self.grid_rowconfigure(99, minsize=10)

    def update_buttons(self, items, cols=3):
        for btn in self.buttons:
            btn.destroy()
        self.buttons = []
        self.items = items
        rows = math.ceil(len(items)/cols)
        col, row = 0, 0
        for item in items:
            name = item
            icon = None
            state = NORMAL
            fg = None
            bg = None
            compound=CENTER
            if type(item) is dict:
                name = item['name']
                icon = item.get('icon', None)
                state = DISABLED if item.get('disabled', False) else NORMAL
                fg = item.get('fgcolor', None)
                bg = item.get('bgcolor', None)
                compound = item.get('compound', CENTER)
            targ_col = 1 + col*2
            targ_row = 3 + row*2
            if not icon:
                icon = ""
            img = self.master.get_image(icon)
            cmd = lambda x=name: self.callback(x)
            btn = Button(self, text=name, image=img, compound=compound, fg=fg, bg=bg, state=state, command=cmd)
            btn.grid(column=targ_col, row=targ_row, sticky=N+E+W)
            self.buttons.append(btn)
            row += 1
            if row >= rows:
                col += 1
                row = 0
        for col in range(cols*2+1):
            if (col % 2) == 0:
                self.grid_columnconfigure(col, minsize=10)
            else:
                self.grid_columnconfigure(col, weight=1)
        for row in range(2, rows+5, 2):
            self.grid_rowconfigure(row+2, minsize=10)

    def handle_button_back(self):
        self.master.screen_pop()

    def handle_button_select(self, item):
        pass

