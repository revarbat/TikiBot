import math
from feeds import SupplyFeed
from recipes import Recipe
from select_screen import SelectScreen
from recipe_screen import RecipeScreen


class ByIngredientScreen(SelectScreen):
    def __init__(self, master):
        self.master = master
        feednames = [x.getName() for x in SupplyFeed.getAll()]
        cols = max(2, math.ceil(len(feednames)/7))
        super(ByIngredientScreen, self).__init__(master, feednames, labeltext="Find drinks by ingredient:", cols=cols)

    def handle_button_select(self, item):
        feed = SupplyFeed.getByName(item)
        recipes = Recipe.getRecipesByFeed(feed)
        self.master.screen_push(RecipeScreen(self.master, recipes, "Select a drink with %s:" % item))

