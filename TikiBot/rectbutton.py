try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa


class RectButton(Button):
    def __init__(self, master, **kwargs):
        self.img = PhotoImage(width=1, height=1)
        super(RectButton, self).__init__(master, image=self.img, compound=CENTER, **kwargs)

