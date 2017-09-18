try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

import math
import operator
from recipes import Recipe, type_icons
from select_screen import SelectScreen
from recipe_edit_screen import RecipeEditScreen
from alpha_screen import AlphaScreen


class ManageRecipesScreen(SelectScreen):
    def __init__(self, master):
        self.master = master
        self.cols = 3
        button_configs = self._calc_buttons()
        super(ManageRecipesScreen, self).__init__(master, button_configs, labeltext="Select a recipe to edit:", cols=self.cols)

    def _calc_buttons(self):
        items = Recipe.getAll()
        button_configs = [
            {"name": item.getName()}
            for item in sorted(items, key=operator.attrgetter('name'))
        ]
        self.cols = max(2, math.ceil(len(button_configs)/7))
        return button_configs

    def activate(self):
        button_configs = self._calc_buttons()
        self.update_buttons(button_configs, self.cols)

    def handle_button_select(self, name):
        recipe = Recipe.getByName(name)
        self.master.screen_push(RecipeEditScreen(self.master, recipe))

    def handle_button_new(self):
        try:
            for n in range(99):
                name = "Recipe %d" % (n+1)
                Recipe.getByName(name)
        except KeyError:
            pass
        self.master.screen_push(AlphaScreen(self.master, label="Name for New Recipe:", defval=name, callback=self._new_recipe_finish))

    def _new_recipe_finish(self, name):
        for typ in type_icons.keys():
            break
        recipe = Recipe(typ, name)
        self.master.screen_pop()
        self.master.screen_push(RecipeEditScreen(self.master, recipe))


