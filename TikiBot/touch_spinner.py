try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton


class TouchSpinner(Frame):
    def __init__(self, master, value=0, values=None, minval=0, maxval=100, incdecval=1, format="%s", justify=CENTER, **kwargs):
        super(TouchSpinner, self).__init__(master, class_="TouchSpinner")
        self.master = master
        self.value = value
        self.values = values
        self.min_value = minval
        self.max_value = maxval
        self.format = format
        self.justify = justify
        self.incdecval = incdecval
        self.changecmd = None

        self.upbtn = RectButton(self, text="+", repeatdelay=500, repeatinterval=100, command=self._button_up)
        self.vallbl = Label(self, text=format % value, justify=justify)
        self.dnbtn = RectButton(self, text="−", repeatdelay=500, repeatinterval=100, command=self._button_dn)

        self.upbtn.pack(side=TOP, fill=X)
        self.dnbtn.pack(side=BOTTOM, fill=X)
        self.vallbl.pack(side=LEFT, fill=BOTH, expand=1)

        self.config(**kwargs)
        self._refresh_label()

    def _button_up(self):
        if self.values:
            try:
                idx = min(self.values.index(self.value)+1, len(self.values))
            except:
                idx = 0
            newval = self.values[idx] if self.values else ""
        else:
            newval = min(self.value + self.incdecval, self.max_value)
        self.set(newval)

    def _button_dn(self):
        if self.values:
            try:
                idx = max(self.values.index(self.value)-1, 0)
            except:
                idx = 0
            newval = self.values[idx] if self.values else ""
        else:
            newval = max(self.value - self.incdecval, self.min_value)
        self.set(newval)

    def _refresh_label(self):
        valstr = self.format % self.value
        self.vallbl.config(text=valstr)

    def get(self):
        return self.value

    def set(self, value):
        oldval = self.value
        self.value = value
        self._refresh_label()
        if callable(self.changecmd):
            self.changecmd(oldval, value)

    def config(self, value=None, minval=None, maxval=None, justify=CENTER, format=None, incdecval=None, changecmd=None, width=None, state=None):
        if value is not None:
            self.set(value)
        if minval is not None:
            self.min_value = minval
        if maxval is not None:
            self.max_value = maxval
        if justify is not None:
            self.justify = justify
        if format is not None:
            self.format = format
            self._refresh_label()
        if incdecval is not None:
            self.incdecval = incdecval
        if changecmd is not None:
            self.changecmd = changecmd
        if width is not None:
            self.upbtn.config(width=width)
            self.dnbtn.config(width=width)
        if state is not None:
            self.upbtn.config(state=state)
            self.dnbtn.config(state=state)
            self.vallbl.config(state=state)


