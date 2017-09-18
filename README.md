TikiBot
=======
Touchscreen BarBot software for auto-dispensing mixed drinks.


Configuration Files
-------------------
`feeds_config.yaml`: Configurations for the feed supply lines.

`recipes_config.yaml`: Recipes and their ingredients.


Code Entrypoint
---------------
`gui.py` is the main file to run to launch this application.


Screens Layout
--------------
Here's the hierarchy of GUI screens for the application.  The button name that leads to a screen is in "quotes".  If a screen is a subclass of another screen class, the base class is in (parens).

    MainScreen
        "Juices" RecipeScreen(SelectScreen)
            PourScreen
                "Pour" DispensingScreen
        "Tiki Drinks" RecipeScreen(SelectScreen)
            PourScreen
                "Pour" DispensingScreen
        "By Ingredient" ByIngredientScreen(SelectScreen)
            PourScreen
                "Pour" DispensingScreen
        "⚙" LockScreen
            ConfigScreen
                "Manage Feeds" ManageFeedsScreen(SelectScreen)
                    FeedScreen
                        "Rename Feed" AlphaScreen
                        "Calibrate" CalibScreen
                "Manage Recipes" ManageRecipesScreen(SelectScreen)
                    "+" AlphaScreen
                    RecipeEditScreen
                        "Recipe:" AlphaScreen
                        "Category:" AlphaScreen
                        "+" SelectScreen
                        "-" SelectScreen
                        "✎" AmountScreen
                "Dump All Feeds" DumpScreen
                "Shutdown" ShutdownScreen

