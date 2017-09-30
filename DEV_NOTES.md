Developer Notes
===============

Screens Concept
---------------
The touchscreen user interface is based around the idea of a stack
of screens, something like old HyperCard.

- `screen_push(newscreen)`:
    pushes a new screen onto the stack.

- `screen_pop()`:
    pops the topmost screen off of the stack.

- `activate()`:
    This method called on a screen class when that screen
    becomes the topmost screen, either through push or pop.
    This allows for updating the content of the screen after
    another screen has been popped off the top of the stack.


Touchscreen Widgets
-------------------
These are widgets that can be used in the creation of a screen.

- RectButton
    Provides a rectangular button on all platforms.

- TouchCheckbox:
    Provides a slider-switch visual version of the standard
    CheckButton.  Slightly prettier and more touchscreen friendly.

- TouchSpinner:
    Provides a basic increment/decrement Spinner widget that is
    more touchscreen friendly.


Generic Screens
---------------
There's a few generic screens that are used in multiple places:

- SelectScreen:
    Given a list of strings, shows buttons for each one, with
    a callback that gets passed the text of the button pressed.
    This is sometimes used as a confirmation screen by just giving
    it a ["Confirm"] button and a text message to display.

- AlphaScreen:
    Provides a touchscreen keyboard for text entry and editing.

- ListScreen:
    Provides a way to edit a list of arbitrary size, through callbacks.
    Can add, delete, edit, and re-order items with standard buttons.

- NotifyScreen:
    Displays a message for the user to see and dismiss.

- LockScreen:
    Dispays a numeric keypad to allow entry or setting of keycodes.


Screens Layout
--------------
Here's the hierarchy of GUI screens for the application.  The button
name that leads to a screen is in "quotes".  If a screen is a
subclass of another screen class, the base class is in (parens).

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
                "Manage Feeds" ManageFeedsScreen(ListScreen)
                    "+" AlphaScreen
                        "Select" FeedEditScreen
                            "Rename Feed" AlphaScreen
                            "Calibrate" CalibScreen
                    "-" SelectScreen
                    "✎" FeedEditScreen [see above]
                "Manage Recipes" ManageRecipesScreen(ListScreen)
                    "+" AlphaScreen
                        "Select" RecipeEditScreen
                            "Recipe:" AlphaScreen
                            "Category:" AlphaScreen
                            "+" SelectScreen
                            "-" SelectScreen
                            "✎" AmountScreen
                    "-" SelectScreen
                    "✎" RecipeEditScreen [see above]
                "Dump All Feeds" DumpScreen
                "Change Passcode" LockScreen
                    NotifyScreen
                "Shutdown" ShutdownScreen


