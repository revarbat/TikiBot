try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton
from alpha_screen import AlphaScreen
from select_screen import SelectScreen
from amount_screen import AmountScreen
from recipes import Recipe, OZ
from feeds import SupplyFeed


class RecipeEditScreen(Frame):
    def __init__(self, master, recipe):
        super(RecipeEditScreen, self).__init__(master)
        self.master = master
        self.recipe = recipe
        self.newfeed = None

        self.renamebtn = RectButton(self, text="Recipe: %s" % recipe.getName(), width=200, justify=LEFT, command=self.handle_button_rename)
        self.retypebtn = RectButton(self, text="Category: %s" % recipe.getType(), width=200, justify=LEFT, command=self.handle_button_retype)
        self.upbtn = RectButton(self, text="\u25b2", state=DISABLED, repeatdelay=500, repeatinterval=100, command=self.handle_button_up)
        self.ingrlb = Listbox(self, width=40, height=5)
        self.dnbtn = RectButton(self, text="\u25bc", state=DISABLED, repeatdelay=500, repeatinterval=100, command=self.handle_button_dn)
        self.recipedel = RectButton(self, text="Delete Recipe", width=150, command=self.handle_button_recipe_del)
        self.ingradd = RectButton(self, text="\u2795", width=50, command=self.handle_button_ingr_add)
        self.ingramt = RectButton(self, text="\u270e", width=50, command=self.handle_button_ingr_amt)
        self.ingrdel = RectButton(self, text="\u2796", width=50, command=self.handle_button_ingr_del)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)
        self.ingrlb.bind('<<ListboxSelect>>', self.ingredient_listbox_select)

        self.renamebtn.grid(column=1, row=1, pady=10, sticky=N+E+W)
        self.retypebtn.grid(column=3, row=1, pady=10, sticky=N+E+W)
        self.upbtn.grid(column=1, row=3, sticky=S+E+W)
        self.ingrlb.grid(column=1, row=4, rowspan=5, padx=2, pady=1, sticky=N+S+E+W)
        self.dnbtn.grid(column=1, row=9, sticky=N+E+W)
        self.recipedel.grid(column=3, row=3, pady=0, sticky=N+E)
        self.ingradd.grid(column=3, row=5, pady=10, sticky=N+W)
        self.ingramt.grid(column=3, row=6, pady=0, sticky=N+W)
        self.ingrdel.grid(column=3, row=7, pady=10, sticky=N+W)
        backbtn.grid(column=3, row=9, sticky=S+E)

        self.columnconfigure(0, minsize=10)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, minsize=10)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, minsize=10)

        self.rowconfigure(0, minsize=10)
        self.rowconfigure(2, minsize=15)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(99, minsize=10)
        self.update_ingr_listbox()

    def handle_button_rename(self):
        self.master.screen_push(AlphaScreen(self.master, label="Name for Recipe:", defval=self.recipe.getName(), callback=self.rename_complete))

    def handle_button_retype(self):
        self.master.screen_push(SelectScreen(self.master, Recipe.getPossibleTypeNames(), labeltext="Select the recipe type:", callback=self.retype_complete))

    def handle_button_recipe_del(self):
        self.master.screen_push(SelectScreen(self.master, ["Confirm"], labeltext="Are you sure you want to delete this recipe?", callback=self.recipe_delete_complete))

    def recipe_delete_complete(self, confirm):
        if confirm == "Confirm":
            self.recipe.delete_recipe()
            self.master.save_configs()
            self.master.screen_pop()
        self.master.screen_pop()

    def update_scroll_btns(self):
        start, end = self.ingrlb.yview()
        self.upbtn.config(state=DISABLED if start == 0.0 else NORMAL)
        self.dnbtn.config(state=DISABLED if end == 1.0 else NORMAL)

    def handle_button_up(self):
        self.ingrlb.yview_scroll(-5, UNITS)
        self.after(100, self.update_scroll_btns)

    def handle_button_dn(self):
        self.ingrlb.yview_scroll(5, UNITS)
        self.after(100, self.update_scroll_btns)

    def ingredient_listbox_select(self, ev=None):
        selidx = self.ingrlb.curselection()
        if not selidx:
            self.sel_ingr = None
        else:
            self.sel_ingr = self.recipe.ingredients[selidx[0]]

    def handle_button_ingr_add(self):
        currfeeds = [ingr.feed.name for ingr in self.recipe.ingredients]
        feeds = [feed for feed in SupplyFeed.getNames() if feed not in currfeeds]
        self.master.screen_push(SelectScreen(self.master, feeds, labeltext="Select the ingredient:", callback=self.add_ingredient_step1))

    def add_ingredient_step1(self, feedname):
        self.newfeed = feedname
        self.master.screen_push(AmountScreen(self.master, whole=1, unit="ounce", labeltext="Select the amount:", callback=self.add_ingredient_step2))

    def add_ingredient_step2(self, ml):
        self.recipe.add(self.newfeed, ml)
        self.newfeed = None
        self.update_ingr_listbox()
        self.master.screen_pop()
        self.master.screen_pop()

    def handle_button_ingr_del(self):
        self.master.screen_push(SelectScreen(self.master, ["Confirm"], labeltext="Are you sure you want to delete that ingredient?", callback=self.del_ingredient_step1))

    def del_ingredient_step1(self, confirm):
        if confirm == "Confirm":
            self.recipe.ingredients.remove(self.sel_ingr)
            self.update_ingr_listbox()
        self.master.screen_pop()

    def handle_button_ingr_amt(self):
        whole, frac, unit = self.sel_ingr.fractionalBarUnits()
        self.master.screen_push(AmountScreen(self.master, whole=whole, frac=frac, unit=unit, labeltext="Select the amount:", callback=self.edit_ingredient_step1))

    def edit_ingredient_step1(self, amt):
        self.sel_ingr.milliliters = amt
        self.update_ingr_listbox()
        self.master.screen_pop()

    def update_ingr_listbox(self):
        self.ingrlb.delete(0, END)
        for ingr in self.recipe.ingredients:
            self.ingrlb.insert(END, ingr.readableDesc())
        self.ingrlb.focus()
        self.ingrlb.selection_clear(0, END)
        self.ingrlb.selection_anchor(0)
        self.ingrlb.selection_set(0)
        self.ingrlb.activate(0)
        self.ingrlb.see(0)
        self.ingredient_listbox_select()
        self.after(100, self.update_scroll_btns)

    def handle_button_back(self):
        self.master.save_configs()
        self.master.screen_pop()

    def rename_complete(self, val):
        self.recipe.rename(val)
        self.renamebtn.config(text="Recipe: %s" % self.recipe.getName())
        self.master.save_configs()
        self.master.screen_pop()

    def retype_complete(self, val):
        self.recipe.retype(val)
        self.retypebtn.config(text="Category: %s" % self.recipe.getType())
        self.master.save_configs()
        self.master.screen_pop()


