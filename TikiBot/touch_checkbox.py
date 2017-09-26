try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa


class TouchCheckbox(Checkbutton):
    def __init__(self, master, **kwargs):
        self.master = master
        toplev = master.winfo_toplevel()
        if 'relief' not in kwargs:
            kwargs['relief'] = FLAT
        if 'compound' not in kwargs:
            kwargs['compound'] = LEFT
        if 'pady' not in kwargs:
            kwargs['pady'] = 2
        if 'padx' not in kwargs:
            kwargs['padx'] = 5
        if 'indicatoron' not in kwargs:
            kwargs['indicatoron'] = False
        if 'image' not in kwargs:
            kwargs['image'] = toplev.get_image("SwitchOff.gif")
        if 'selectimage' not in kwargs:
            kwargs['selectimage'] = toplev.get_image("SwitchOn.gif")
        super(TouchCheckbox, self).__init__(master, **kwargs)


