TikiBot
=======
Touchscreen BarBot software for auto-dispensing mixed drinks.


Hardware
--------
This software has been tested with the following hardware:

- Udoo Neo ( [source](https://www.udoo.org) )
- 7" 800x480 Touchscreen HDMI display
- 3 Adafruit DC Motor Featherwings ( [source](https://www.adafruit.com/product/2927) )
- 12 Small self-priming pumps ( [source](http://www.trossenrobotics.com/robotgeek-pump-small) )
- 12 Normally Closed solonoid valves ( [source](https://www.amazon.com/dp/B007D1U64E/ref=cm_sw_r_tw_dp_x_qDVWzbPCEW4K5) )

Each DC Motor controller handles up to 4 feeds.  Each motor controller will
need to have a consecutive different I2C address. You can alternately use
the following DC motor controllers without changing any code:

- Adafruit DC & Stepper Motor HAT for Raspberry Pi ( [source](https://www.adafruit.com/product/2348) )
- Adafruit Motor/Stepper/Servo Shield for Arduino v2 ( [source](https://www.adafruit.com/product/1438) )

It should be trivial to use a Raspberry Pi instead of the Udoo Neo.
Probably the easiest configuration would be to use a Raspberry Pi
with a few stacked DC Motor HATs.

Each feed is a paired pump and valve, wired in parallel.
Each pump/valve combo should be wired and plumbed as follows:

![Pump/Valve wiring](imgsrcs/PumpValveWiring.png)

The polarity of the wiring is irrelevant for the linked pumps and
valves.  For them, either polarity will result in the forward pump
action with the valve open.


Configuration Files
-------------------
`resources/tikibot_configs.yaml`: Contains all configs for passcode,
feeds, recipes, etc.

In the lower right corner of the main screen is a gear icon.  This is
the configuration menu button. If you press it, it will ask for an
administrative passcode.  The default is '8888'.  Once you enter the
correct passcode, you will be shown the configuration screen.  From
here, you can change the passcode (recommended!), add, edit and re-order
feeds, add, and edit drink recipes, and shutdown or reboot the system.
Any changes made here will be saved to the `tikibot_configs.yaml` file.


Code Entrypoint
---------------
`gui.py` is the main file to run to launch this application.


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
                "Manage Feeds" ManageFeedsScreen(SelectScreen)
                    "+" AlphaScreen
                    FeedScreen
                        "Delete Feed" SelectScreen
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
                "Change Passcode" LockScreen
                    NotifyScreen
                "Shutdown" ShutdownScreen

