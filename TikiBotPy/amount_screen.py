try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton
from touch_spinner import TouchSpinner
from recipes import unit_measures


class AmountScreen(Frame):
    def __init__(self, master, labeltext="Select an amount:", seltext="Select", whole=1, frac="", unit="ounce", callback=None):
        super(AmountScreen, self).__init__(master, class_="Amount")
        self.master = master
        self.callback = callback
        fracvals = ["", "1/8", "1/4", "1/3", "3/8", "1/2", "5/8", "2/3", "3/4", "7/8"]
        unitvals = ["dash", "ml", "tsp", "tbsp", "ounce", "cup"]

        lbl = Label(self, text=labeltext)
        self.wholespin = TouchSpinner(self, width=40, value=whole, minval=0, maxval=99, incdecval=1, justify=RIGHT)
        self.fracspin = TouchSpinner(self, width=40, value=frac, values=fracvals)
        self.unitspin = TouchSpinner(self, width=40, value=unit, values=unitvals, justify=LEFT)
        selbtn = RectButton(self, text=seltext, width=120, command=self.handle_button_select)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)

        lbl.grid(column=1, row=1, columnspan=3, padx=20, pady=10, sticky=N+E+W)
        self.wholespin.grid(column=1, row=2, padx=5, pady=20, sticky=N+E)
        self.fracspin.grid(column=2, row=2, padx=5, pady=20, sticky=N)
        self.unitspin.grid(column=3, row=2, padx=5, pady=20, sticky=N+W)
        selbtn.grid(column=1, row=9, padx=20, pady=10, sticky=S+W)
        backbtn.grid(column=3, row=9, padx=20, pady=10, sticky=S+E)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, minsize=10)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(10, minsize=10)

    def handle_button_select(self):
        self.master.save_configs()
        numer, denom = 0, 1
        val = float(self.wholespin.get())
        frac = self.fracspin.get()
        if frac:
            numer, denom = frac.split("/")
        val += float(numer) / float(denom)
        val *= unit_measures[self.unitspin.get()]
        if callable(self.callback):
            self.callback(val)
        else:
            self.master.screen_pop()

    def handle_button_back(self):
        self.master.screen_pop()


