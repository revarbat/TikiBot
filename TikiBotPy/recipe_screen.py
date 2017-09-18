import math
from recipes import Recipe
from pour_screen import PourScreen
from select_screen import SelectScreen


class RecipeScreen(SelectScreen):
    def __init__(self, master, recipes, labeltext):
        self.recipes = recipes
        buttons = [
            {
                'name': recipe.getName(),
                'icon': recipe.getIcon(),
                'disabled': not recipe.canMake(),
            }
            for recipe in recipes
        ]
        cols = max(2, math.ceil(len(buttons)/7))
        super(RecipeScreen, self).__init__(master, buttons, labeltext=labeltext, cols=cols)

    def handle_button_select(self, item):
        recipe = Recipe.getByName(item)
        self.master.screen_push(PourScreen(self.master, recipe))

