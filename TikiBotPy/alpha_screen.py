try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton


class AlphaScreen(Frame):
    def __init__(self, master, label="Enter text:", defval="", callback=None):
        self.callback = callback if callback else self.master.screen_pop
        self.label_txt = label
        self.curr_kbfr = None
        self.kbframes = []
        super(AlphaScreen, self).__init__(master, class_="Alpha")

        if self.label_txt:
            self.lbl = Label(self, text=self.label_txt, font="Helvetica 24")
        self.entry = Entry(self, width=30, font="Helvetica 24")
        self.entry.delete(0, END)
        self.entry.insert(0, defval)
        self.entry.icursor(END)

        if self.label_txt:
            self.lbl.pack(side=TOP, fill=X, expand=0, padx=10, pady=20)
        self.entry.pack(side=TOP, fill=NONE, expand=1)

        keyboards = [
            [
                ["q", "u", "e", "r", "t", "y", "u", "i", "o", "p"],
                ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
                ["ABC", "z", "x", "c", "v", "b", "n", "m", "\u232b"],
                ["123", "\u2190", "\u2192", "Space", "Cancel", "Enter"]
            ],
            [
                ["Q", "U", "E", "R", "T", "Y", "U", "I", "O", "P"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
                ["abc", "Z", "X", "C", "V", "B", "N", "M", "\u232b"],
                ["123", "\u2190", "\u2192", "Space", "Cancel", "Enter"]
            ],
            [
                ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                ["-", "/", ":", ";", "(", ")", "$", "&", "@", '"'],
                ["abc", ".", ",", "?", "!", "'", "\u232b"],
                ["*%^", "\u2190", "\u2192", "Space", "Cancel", "Enter"]
            ],
            [
                ["[", "]", "{", "}", "#", "%", "^", "*", "+", "="],
                ["_", "\\", "|", "~", "<", ">", "\u20ac", "\u00a3", "\u00a5", '\u00b7'],
                ["abc", ".", ",", "?", "!", "'", "\u232b"],
                ["123", "\u2190", "\u2192", "Space", "Cancel", "Enter"]
            ],
        ]
        key_widths = {
            "\u2190": 50,
            "\u2192": 50,
            "Space": 500,
            "Cancel": 150,
            "Enter": 150,
        }
        for kb in keyboards:
            kbfr = Frame(self)
            self.kbframes.append(kbfr)
            for keyrow in kb:
                rowfr = Frame(kbfr)
                for col, key in enumerate(keyrow):
                    keywidth = key_widths.get(key, 100)
                    keybtn = RectButton(rowfr, text="%s" % key, height=40, repeatdelay=500, repeatinterval=100, command=lambda x=key:self.handle_button_key(x))
                    keybtn.grid(column=col, row=0, sticky=E+W, padx=5, pady=5)
                    rowfr.columnconfigure(col, weight=keywidth)
                rowfr.pack(side=TOP, fill=X, expand=1)
        self.change_kb(0)

    def change_kb(self, num):
        if self.curr_kbfr and self.curr_kbfr != self.kbframes[num]:
            self.curr_kbfr.forget()
        self.curr_kbfr = self.kbframes[num]
        self.curr_kbfr.pack(side=BOTTOM, fill=X, expand=0, padx=5, pady=5)
        self.entry.focus()

    def handle_button_key(self, key):
        if key == "Cancel":
            self.master.screen_pop()
            return
        if key == "Enter":
            val = self.entry.get()
            self.callback(val)
            return
        if key == "\u2190":  # Left arrow
            idx = self.entry.index(INSERT)
            idx = (idx - 1) if idx > 0 else idx
            self.entry.icursor(idx)
            return
        if key == "\u2192":  # Right arrow
            txtlen = len(self.entry.get())
            idx = self.entry.index(INSERT)
            idx = (idx + 1) if idx < txtlen else idx
            self.entry.icursor(idx)
            return
        if key == "\u232b":  # Delete key
            idx = self.entry.index(INSERT)
            if idx > 0:
                self.entry.delete(idx-1)
            return
        if key == "abc":
            self.change_kb(0)
            return
        if key == "ABC":
            self.change_kb(1)
            return
        if key == "123":
            self.change_kb(2)
            return
        if key == "*%^":
            self.change_kb(3)
            return
        if key == "Space":
            key = " "
        self.entry.insert(INSERT, key)


