from __future__ import division

import sys
import math
import time
import platform
import operator
from feeds import SupplyFeed


# Unit multipliers to convert to milliliters
GALLON = 3785.41
QUART = 946.35
FIFTH = 757.08
PINT = 473.17
CUP = 236.58
SHOT = 44.36
JIGGER = 44.36
PONY = 29.57
OUNCE = 29.57
OZ = 29.57
TBSP = 14.79
TSP = 4.93
SPLASH = 2.5
DASH = 0.92
MILLILITER = 1.0
CENTILITER = 10.0
DECILITER = 100.0
LITER = 1000.0
ML = 1.0
CL = 10.0
DL = 100.0
L = 1000.0


unit_measures = {
    "dash": DASH,
    "splash": SPLASH,
    "tsp": TSP,
    "tbsp": TBSP,
    "oz": OZ,
    "ounce": OUNCE,
    "pony": PONY,
    "jigger": JIGGER,
    "shot": SHOT,
    "cup": CUP,
    "pint": PINT,
    "fifth": FIFTH,
    "quart": QUART,
    "gallon": GALLON,
    "ml": ML,
    "cl": CL,
    "dl": DL,
    "l": L,
}


type_icons = {
    "Juices": "JuicesIcon.gif",
    "Tiki Drinks": "TikiDrinkIcon.gif",
    "Cocktails": "CocktailsIcon.gif",
}


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Ingredient(object):
    def __init__(self, feed, ml):
        self.feed = feed
        self.milliliters = ml

    @classmethod
    def fromArray(cls, data):
        if type(data) is dict:
            name = data['name']
            ml = data['ml']
        else:
            name, amount, unit = data
            mult = unit_measures.get(unit, 0.0)
            ml = amount * mult
        feed = SupplyFeed.getByName(name)
        return cls(feed, ml)

    def toArray(self):
        val, unit = self.getBarUnits()
        return [self.feed.getName(), val, unit]

    def getName(self):
        return self.feed.getName()

    def getBarUnits(self, partial=1.0):
        ml = self.milliliters * partial
        unit, div = ("dash", DASH)
        if ml > 0.25 * OZ:
            unit, div = ("oz", OZ)
        elif ml > TBSP:
            unit, div = ("Tbsp", TBSP)
        elif ml > 2*DASH:
            unit, div = ("tsp", TSP)
        val = ml / div
        return (val, unit)

    def fractionalBarUnits(self, partial=1.0):
        val, unit = self.getBarUnits(partial)
        whole = math.floor(val)
        frac = val - whole
        min_delta = 1
        found_numer = 0
        found_denom = 0
        for denom in [8, 6, 4, 3, 2]:
            numer = math.floor((frac * denom) + 0.5)
            delta = abs(frac - (numer/denom))
            if delta <= min_delta:
                min_delta = delta
                found_numer = numer
                found_denom = denom
        if found_numer >= found_denom:
            found_numer -= found_denom
            whole += 1
        frac = ""
        if found_numer > 0:
            frac = "%d/%d" % (found_numer, found_denom)
        return (whole, frac, unit)

    def readableDesc(self, partial=1.0):
        whole, frac, unit = self.fractionalBarUnits(partial=partial)
        valstr = ""
        if whole > 0:
            valstr += "%d" % whole
        if frac:
            if valstr:
                valstr += " "
            valstr += frac
        if not valstr:
            valstr = "0"
        return "%s %s %s" % (valstr, unit, self.getName())

    def isFlowing(self):
        return self.feed.isFlowing()

    def startFeed(self):
        self.feed.startFeed()

    def stopFeed(self):
        self.feed.stopFeed()


class DispensingIngredient(Ingredient):
    def __init__(self, ingr, size_mult, max_time):
        new_vol = ingr.milliliters * size_mult
        super(DispensingIngredient, self).__init__(ingr.feed, new_vol)
        self.dispensed = 0.0
        self.proportion = (new_vol / ingr.feed.flowrate) / max_time

    def done(self):
        return self.dispensed >= self.milliliters

    def percentDone(self):
        return 100.0 * self.dispensed / self.milliliters

    def updateDispensed(self, secs):
        self.dispensed  += self.feed.flowrate * secs


class UnknownRecipeTypeError(Exception):
    pass


class Recipe(object):
    recipes = {}
    recipe_types = {}
    by_feed = {}

    def __init__(self, type_, name, ingredients=[], icon=None):
        global type_icons
        if type_ not in type_icons:
            raise UnknownRecipeTypeError()
        if type_ not in Recipe.recipe_types:
            Recipe.recipe_types[type_] = []
        Recipe.recipe_types[type_].append(self)
        self.type_ = type_
        self.name = name
        self.icon = icon
        self.ingredients = []
        self.dispensing = []
        self.timeslice_secs = 1.0
        self.min_dispense_secs = 0.1
        self.last_timeslice = time.time()
        self.last_update_time = time.time()
        Recipe.recipes[name] = self
        for ingr_data in ingredients:
            ingr = Ingredient.fromArray(ingr_data)
            feedname = ingr.feed.getName()
            if feedname not in Recipe.by_feed:
                Recipe.by_feed[feedname] = []
            Recipe.by_feed[feedname].append(self)
            self.ingredients.append(ingr)

    @classmethod
    def fromDict(cls, d):
        """Create new Recipe instances from a dictionary description."""
        global type_icons
        if 'type_icons' in type_icons:
            type_icons = d['type_icons']
        # Delete old Recipes
        for name, recipe in cls.recipes.items():
            recipe.delete_recipe()
        # Add Recipes from dict
        for name, data in d.get('recipes', {}).items():
            cls(
                data['type'],
                name,
                data['ingredients'],
                icon=data.get('icon')
            )

    @classmethod
    def toDictAll(cls, d):
        """Create a dictionary description of all Recipe instances."""
        global type_icons
        d['recipes'] = {name: recipe.toDict() for name, recipe in cls.recipes.items()}
        d['type_icons'] = type_icons
        return d

    def toDict(self):
        data = {
            'type': self.type_,
            'ingredients': [x.toArray() for x in self.ingredients]
        }
        if self.icon:
            data['icon'] = self.icon
        return data

    @classmethod
    def getTypeNames(cls):
        return sorted(cls.recipe_types.keys())

    @staticmethod
    def getPossibleTypeNames():
        global type_icons
        return sorted(type_icons.keys())

    @classmethod
    def getTypeIcon(cls, name):
        global type_icons
        return type_icons[name]

    @classmethod
    def getRecipesByType(cls, name):
        recipe_list = cls.recipe_types[name]
        return sorted(recipe_list, key=operator.attrgetter('name'))

    @classmethod
    def getRecipesByFeed(cls, name):
        if name not in cls.by_feed:
            return []
        recipe_list = cls.by_feed[name]
        return sorted(recipe_list, key=operator.attrgetter('name'))

    @classmethod
    def getNames(cls):
        return sorted(cls.recipes.keys())

    @classmethod
    def getAll(cls):
        for key in sorted(cls.recipes.keys()):
            yield cls.recipes[key]

    @classmethod
    def getByName(cls, name):
        return cls.recipes[name]

    def getName(self):
        return self.name

    def getType(self):
        return self.type_

    def getIcon(self):
        return self.icon

    def delete_recipe(self):
        del Recipe.recipes[self.name]
        Recipe.recipe_types[self.type_].remove(self)
        if not Recipe.recipe_types[self.type_]:
            del Recipe.recipe_types[self.type_]
        for ingr in self.ingredients:
            feedname = ingr.feed.getName()
            Recipe.by_feed[feedname].remove(self)
            if not Recipe.by_feed[feedname]:
                del Recipe.by_feed[feedname]

    def rename(self, newname):
        del Recipe.recipes[self.name]
        self.name = newname
        Recipe.recipes[newname] = self

    def retype(self, newtype):
        global type_icons
        if newtype not in type_icons:
            raise UnknownRecipeTypeError()
        if newtype not in Recipe.recipe_types:
            Recipe.recipe_types[newtype] = []
        Recipe.recipe_types[self.type_].remove(self)
        if not Recipe.recipe_types[self.type_]:
            del Recipe.recipe_types[self.type_]
        self.type_ = newtype
        Recipe.recipe_types[newtype].append(self)

    def add(self, feedname, ml):
        feed = SupplyFeed.getByName(feedname)
        self.ingredients.append(Ingredient(feed, ml))
        return self

    def canMake(self):
        for ingr in self.ingredients:
            if not ingr.feed.avail:
                return False
        return True

    def totalVolume(self):
        vol = 0.0
        for ingr in self.ingredients:
            vol += ingr.milliliters
        return vol

    def startDispensing(self, volume):
        tot_vol = self.totalVolume()
        vol_mult = volume / tot_vol
        self.dispensing = []
        max_time = max([vol_mult * x.milliliters / x.feed.flowrate for x in self.ingredients])
        for ingr in self.ingredients:
            self.dispensing.append(DispensingIngredient(ingr, vol_mult, max_time))
        for ingr in self.dispensing:
            ingr.startFeed()
        self.last_update_time = time.time()
        self.last_timeslice = 0
        self.updateDispensing()

    def updateDispensing(self):
        now = time.time()
        secs = now - self.last_update_time
        slice_secs = now - self.last_timeslice
        self.last_update_time = now
        if slice_secs > self.timeslice_secs:
            # Beginning of timeslice.  Start/Restart incomplete feeds.
            self.last_timeslice = now
            for ingr in self.dispensing:
                if not ingr.isFlowing() and not ingr.done():
                    ingr.startFeed()
        else:
            # Mid-timeslice.  Pause proportional feeds.
            for ingr in self.dispensing:
                if not ingr.done() and ingr.isFlowing():
                    ingr.updateDispensed(secs)
                    if ingr.done():
                        if platform.system() != "Linux":
                            eprint("  Feed #%d dispensed: %goz" % (ingr.feed.motor_num, ingr.dispensed/OZ))
                        ingr.dispensed += ingr.feed.pulse_overage
                        ingr.stopFeed()
                    elif slice_secs > max(self.min_dispense_secs, self.timeslice_secs * ingr.proportion):
                        ingr.dispensed += ingr.feed.pulse_overage
                        ingr.stopFeed()
        self.dispensing[:] = [x for x in self.dispensing if not x.done()]

    def cancelDispensing(self):
        for ingr in self.dispensing:
            ingr.dispensed += ingr.feed.pulse_overage
            ingr.stopFeed()

    def doneDispensing(self):
        return not self.dispensing


