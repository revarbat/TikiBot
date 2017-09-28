try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton
from select_screen import SelectScreen


class ListScreen(Frame):
    def __init__(
            self,
            master,
            items_cb,
            label_text="",
            add_cb=None,
            del_cb=None,
            edit_cb=None,
            raise_cb=None,
            lower_cb=None,
            add_lbl="\u2795",
            del_lbl="\u2796",
            edit_lbl="\u270e",
            raise_lbl="\u2b06",
            lower_lbl="\u2b07",
            extra_btns=None
        ):
        super(ListScreen, self).__init__(master)
        self.master = master
        self.items_cb = items_cb
        self.add_cb = add_cb
        self.del_cb = del_cb
        self.edit_cb = edit_cb
        self.raise_cb = raise_cb
        self.lower_cb = lower_cb
        self.extra_btns = []
        self.items = []

        btnwidth = 150
        if label_text:
            self.lbl = Label(self, text=label_text)
        self.upbtn = RectButton(self, text="\u25b2", state=DISABLED, repeatdelay=500, repeatinterval=100, command=self.handle_button_up)
        self.lbox = Listbox(self, width=40, height=5, fg="#000000", bg="#ffffff")
        self.dnbtn = RectButton(self, text="\u25bc", state=DISABLED, repeatdelay=500, repeatinterval=100, command=self.handle_button_dn)
        if self.add_cb:
            self.addbtn = RectButton(self, text=add_lbl, width=btnwidth, command=self.handle_button_add)
        if self.edit_cb:
            self.editbtn = RectButton(self, text=edit_lbl, width=btnwidth, command=self.handle_button_edit)
        if self.del_cb:
            self.delbtn = RectButton(self, text=del_lbl, width=btnwidth, command=self.handle_button_del)
        if self.raise_cb:
            self.raisebtn = RectButton(self, text=raise_lbl, width=btnwidth, command=self.handle_button_raise)
        if self.lower_cb:
            self.lowerbtn = RectButton(self, text=lower_lbl, width=btnwidth, command=self.handle_button_lower)
        if extra_btns:
            self.extra_btns = []
            for d in extra_btns:
                txt = d['name']
                cb = d['callback']
                en = d.get('enable_cb', None)
                btn = RectButton(self, text=txt, width=btnwidth, command=lambda x=cb: self.handle_button_extra(x))
                btn.en_cb = en
                self.extra_btns.append(btn)
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)
        self.lbox.bind('<<ListboxSelect>>', self.listbox_select)

        if label_text:
            self.lbl.grid(column=1, row=1, columnspan=3, sticky=N+W)
        self.upbtn.grid(column=1, row=2, sticky=S+E+W)
        self.lbox.grid(column=1, row=3, rowspan=95, padx=2, pady=1, sticky=N+S+E+W)
        self.dnbtn.grid(column=1, row=98, sticky=N+E+W)
        if self.add_cb:
            self.addbtn.grid(column=3, row=3, pady=5, sticky=N+W)
        if self.edit_cb:
            self.editbtn.grid(column=3, row=4, pady=5, sticky=N+W)
        if self.del_cb:
            self.delbtn.grid(column=3, row=5, pady=5, sticky=N+W)
        if self.raise_cb:
            self.raisebtn.grid(column=3, row=7, pady=5, sticky=N+W)
        if self.lower_cb:
            self.lowerbtn.grid(column=3, row=8, pady=5, sticky=N+W)
        for n, btn in enumerate(self.extra_btns):
            btn.grid(column=3, row=10+n, pady=5, sticky=N+W)
        backbtn.grid(column=3, row=98, sticky=S+E)

        self.columnconfigure(0, minsize=10)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, minsize=10)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, minsize=10)

        self.rowconfigure(0, minsize=10)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(97, weight=1)
        self.rowconfigure(99, minsize=10)

        self.update_listbox()

    def update_listbox(self):
        items = self.items_cb()
        if type(items[0]) in [tuple, list]:
            items = [{"name": name, "data": data} for name, data in items]
        elif type(items[0]) is str:
            items = [{"name": name, "data": None} for name in items]
        self.items = items
        selidx = self.lbox.curselection()
        selidx = selidx[0] if selidx else 0
        if selidx >= len(items):
            selidx = END
        self.lbox.delete(0, END)
        for item in items:
            fg = item.get('fgcolor', None)
            bg = item.get('bgcolor', None)
            fg = fg if fg else "#000000"
            bg = bg if bg else "#ffffff"
            self.lbox.insert(END, item['name'])
            self.lbox.itemconfig(END, foreground=fg)
            self.lbox.itemconfig(END, background=bg)
        self.lbox.focus()
        self.lbox.selection_clear(0, END)
        self.lbox.selection_anchor(selidx)
        self.lbox.selection_set(selidx)
        self.lbox.activate(selidx)
        self.lbox.see(selidx)
        self.listbox_select()
        self.after(100, self.update_button_states)

    def listbox_select(self, ev=None):
        self.sel_idx = None
        self.sel_txt = None
        self.sel_dat = None
        selidx = self.lbox.curselection()
        if selidx:
            selidx = selidx[0]
            item = self.items[selidx]
            self.sel_idx = selidx
            self.sel_txt = item.get('name')
            self.sel_dat = item.get('data')
        self.after(100, self.update_button_states)

    def update_button_states(self):
        start, end = self.lbox.yview()
        selidx = self.lbox.curselection()
        selidx = selidx[0] if selidx else None
        endidx = self.lbox.index(END) - 1 if selidx is not None else None
        self.upbtn.config(state=NORMAL if start > 0.0 else DISABLED)
        self.dnbtn.config(state=NORMAL if end < 1.0 else DISABLED)
        if self.del_cb:
            self.delbtn.config(state=NORMAL if selidx is not None else DISABLED)
        if self.edit_cb:
            self.editbtn.config(state=NORMAL if selidx is not None else DISABLED)
        if self.raise_cb:
            self.raisebtn.config(state=NORMAL if selidx is not None and selidx>0 else DISABLED)
        if self.lower_cb:
            self.lowerbtn.config(state=NORMAL if selidx is not None and selidx<endidx else DISABLED)
        for btn in self.extra_btns:
            btn.config(state=NORMAL if btn.en_cb(selidx) else DISABLED)

    def _scroll(self, n):
        self.lbox.yview_scroll(n, UNITS)
        self.update()
        self.update_button_states()

    def handle_button_up(self):
        for i in range(5):
            self.after(100*i, self._scroll, -1)

    def handle_button_dn(self):
        for i in range(5):
            self.after(100*i, self._scroll, 1)

    def handle_button_add(self):
        self.add_cb()
        self.update_listbox()

    def handle_button_del(self):
        self.del_cb(self.sel_idx, self.sel_txt, self.sel_dat)
        self.update_listbox()

    def handle_button_edit(self):
        self.edit_cb(self.sel_idx, self.sel_txt, self.sel_dat)
        self.update_listbox()

    def handle_button_raise(self):
        self.raise_cb(self.sel_idx, self.sel_txt, self.sel_dat)
        selidx = self.sel_idx - 1 if self.sel_idx > 0 else 0
        self.lbox.selection_clear(0, END)
        self.lbox.selection_anchor(selidx)
        self.lbox.selection_set(selidx)
        self.lbox.activate(selidx)
        self.lbox.see(selidx)
        self.listbox_select()
        self.update_listbox()

    def handle_button_lower(self):
        self.lower_cb(self.sel_idx, self.sel_txt, self.sel_dat)
        endidx = self.lbox.index(END)-1
        selidx = self.sel_idx + 1 if self.sel_idx < endidx else endidx
        self.lbox.selection_clear(0, END)
        self.lbox.selection_anchor(selidx)
        self.lbox.selection_set(selidx)
        self.lbox.activate(selidx)
        self.lbox.see(selidx)
        self.listbox_select()
        self.update_listbox()

    def handle_button_extra(self, cb):
        cb(self.sel_idx, self.sel_txt, self.sel_dat)
        self.listbox_select()
        self.update_listbox()

    def handle_button_back(self):
        self.master.screen_pop()



