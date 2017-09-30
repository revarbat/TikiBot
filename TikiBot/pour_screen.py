try:  # Python 2
    from Tkinter import *  # noqa
    from tkFont import Font
except ImportError:  # Python 3
    from tkinter import *  # noqa
    from tkinter.font import Font

from recipes import Recipe, OZ
from rectbutton import RectButton
from dispensing_screen import DispensingScreen


class PourScreen(Frame):
    def __init__(self, master, recipe):
        super(PourScreen, self).__init__(master, class_="Pour")
        self.master = master
        self.recipe = recipe
        self.pouricon = self.master.get_image("PourIcon.gif")
        self.desc = Text(self, width=32, state=DISABLED)
        lbl = Label(self, text="Amount to dispense:")
        upbtn = RectButton(self, text="+", width=120, repeatdelay=500, repeatinterval=100, command=self.handle_button_up)
        self.selbtn = Button(self, text="\nPour\n6 oz", image=self.pouricon, compound=CENTER, width=120, height=160, command=self.handle_button_sel)
        dnbtn = RectButton(self, text="−", width=120, repeatdelay=500, repeatinterval=100, command=self.handle_button_dn)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)

        self.desc.grid(column=1, row=1, rowspan=7, sticky=N+S+E+W)
        lbl.grid(column=3, row=1, sticky=N)
        upbtn.grid(column=3, row=3, sticky=S)
        self.selbtn.grid(column=3, row=4, pady=5, sticky=N+S)
        dnbtn.grid(column=3, row=5, sticky=N)
        backbtn.grid(column=3, row=7, sticky=S)

        self.grid_columnconfigure(0, minsize=20)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, minsize=20)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, minsize=20)
        self.grid_rowconfigure(0, minsize=20)
        self.grid_rowconfigure(2, minsize=20)
        self.grid_rowconfigure(6, minsize=40)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, minsize=20)

        if self.master.use_metric:
            self.set_amount(25*int(recipe.totalVolume()/25+0.5))
        else:
            self.set_amount(int(recipe.totalVolume()/OZ+0.5))

    def get_amount(self):
        return int(self.selbtn.cget('text').split()[1])

    def set_amount(self, val):
        unit = "ml" if self.master.use_metric else "oz"
        self.selbtn.config(text="\nPour\n%d %s" % (val, unit))
        self.update_recipe_desc()

    def update_recipe_desc(self):
        vol = self.get_amount()
        if not self.master.use_metric:
            vol *= OZ
        total_vol = self.recipe.totalVolume()
        name = self.recipe.getName()
        apbv = self.recipe.getAlcoholPercentByVolume()
        partial = vol / total_vol
        self.desc.config(state=NORMAL)
        self.desc.delete(1.0, END)
        smallfont = Font(family="Helvetica", size=12)
        self.desc.tag_config("recipe", lmargin1=3, rmargin=3, spacing1=2, spacing3=2, background="#077", foreground="white")
        self.desc.tag_config("virgin", lmargin1=3, rmargin=3, spacing1=2, spacing3=2, background="#7f7", foreground="black", font=smallfont)
        self.desc.tag_config("abv", lmargin1=3, rmargin=3, spacing1=2, spacing3=2, background="#ff7", foreground="black", font=smallfont)
        self.desc.insert(END, "%s\n" % name, "recipe")
        for ing in self.recipe.ingredients:
            self.desc.insert(END, "%s\n" % ing.readableDesc(partial, metric=self.master.use_metric))
        self.desc.insert(END, "\n")
        if apbv < 0.1:
            self.desc.insert(END, "Non-Alcoholic\n", "virgin")
        else:
            alc_warn = "\u2620" * int(vol*apbv/100.0/14.0)
            self.desc.insert(END, "%.1f%% Alcohol by Volume  %s\n" % (apbv, alc_warn), "abv")
        self.desc.config(state=DISABLED)
        self.master.update()

    def handle_button_up(self):
        val = self.get_amount()
        incdec = 25 if self.master.use_metric else 1
        maxval = 500 if self.master.use_metric else 16
        if val < maxval:
            val += incdec
        self.set_amount(val)

    def handle_button_dn(self):
        val = self.get_amount()
        incdec = 25 if self.master.use_metric else 1
        if val > incdec:
            val -= incdec
        self.set_amount(val)

    def handle_button_sel(self):
        vol = self.get_amount()
        if not self.master.use_metric:
            vol *= OZ
        self.master.screen_push(DispensingScreen(self.master, self.recipe, vol))

    def handle_button_back(self):
        self.master.screen_pop()

