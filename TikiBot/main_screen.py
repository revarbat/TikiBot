try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import math
from recipes import Recipe
from rectbutton import RectButton
from recipe_screen import RecipeScreen
from lock_screen import LockScreen
from config_screen import ConfigScreen
from byingredient_screen import ByIngredientScreen


class MainScreen(Frame):
    def __init__(self, master):
        super(MainScreen, self).__init__(master, class_="MainScreen")
        self.master = master
        self.buttons = []
        self.update_buttons()

    def update_buttons(self):
        for btn in self.buttons:
            btn.forget()
            btn.destroy()
        types = Recipe.getTypeNames()
        colsarr = [1, 2, 3, 2, 3, 3, 4]
        maxcols = colsarr[len(types)]
        col, row = 1, 1
        for type_ in types:
            img = self.master.get_image(Recipe.getTypeIcon(type_))
            cmd = lambda typ=type_: self.handle_type_button(typ)
            btn = Button(self, text=type_, compound=TOP, image=img, command=cmd, width=160)
            btn.grid(column=col, row=row, padx=5, pady=5)
            self.buttons.append(btn)
            col += 1
            if col > maxcols:
                col = 1
                row += 1
                self.rowconfigure(row, weight=0)
        img = self.master.get_image("IngredientsIcon.gif")
        btn = Button(self, text="By Ingredient", compound=TOP, image=img, command=self.handle_button_ingredients, width=160)
        btn.grid(column=col, row=row, padx=5, pady=5)
        self.buttons.append(btn)
        confbtn = RectButton(self, text="\u2699", command=self.handle_button_conf, width=15, height=20)
        confbtn.grid(column=maxcols, row=row, columnspan=2, rowspan=2, sticky=S+E)
        self.buttons.append(confbtn)
        self.columnconfigure(0, weight=1)
        for col in range(maxcols):
            self.columnconfigure(col+1, weight=0)
        self.columnconfigure(maxcols+1, weight=1)
        self.columnconfigure(maxcols+2, weight=0)
        self.columnconfigure(maxcols+3, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(row+1, weight=1)
        self.rowconfigure(row+2, weight=0)
        self.rowconfigure(row+3, weight=0)

    def activate(self):
        self.update_buttons()

    def handle_type_button(self, type_):
        recipes = Recipe.getRecipesByType(type_)
        self.master.screen_push(RecipeScreen(self.master, recipes, "Choose one of these %s:" % type_))

    def handle_button_ingredients(self):
        self.master.screen_push(ByIngredientScreen(self.master))

    def handle_button_conf(self):
        self.master.screen_push(LockScreen(self.master, ConfigScreen(self.master)))


