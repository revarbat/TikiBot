try:  # Python 2
    from Tkinter import *  # noqa
except ImportError:  # Python 3
    from tkinter import *  # noqa

from rectbutton import RectButton
from touch_spinner import TouchSpinner


class CalibScreen(Frame):
    def __init__(self, master, feed):
        super(CalibScreen, self).__init__(master)
        self.master = master
        self.feed = feed
        self.dispensed = 0.0
        self.target_ml = 0.0
        self.duty_cycle = 1.0
        self.dispensing = False
        self.start_pid = None
        self.stop_pid = None

        lbl = Label(self, text="Feed #%d: %s" % (feed.motor_num, feed.getName()))
        self.dutyspin = TouchSpinner(self, width=150, value=100, minval=10, maxval=100, incdecval=5, format="Duty: %d%%")
        self.amntspin = TouchSpinner(self, width=150, value=100, minval=25, maxval=500, incdecval=25, format="Amount: %d ml")
        self.pourbtn = RectButton(self, text="Pour", width=150, command=self.handle_button_pour)
        self.flowspin = TouchSpinner(self, width=150, value=feed.flowrate, minval=0.1, maxval=50.0, incdecval=0.1, format="Flow: %.1f ml/s", changecmd=self._flowrate_change)
        self.overspin = TouchSpinner(self, width=150, value=feed.pulse_overage, minval=0.0, maxval=2.0, incdecval=0.01, format="Pulse: %.2f ml", changecmd=self._overage_change)
        self.displbl = Label(self, text="")
        backbtn = RectButton(self, text="\u23ce", width=120, command=self.handle_button_back)

        lbl.grid(column=1, row=1, columnspan=3, padx=20, pady=10, sticky=N+E+W)
        self.dutyspin.grid(column=1, row=2, padx=20, pady=20, sticky=N)
        self.amntspin.grid(column=2, row=2, padx=20, pady=20, sticky=N)
        self.pourbtn.grid(column=3, row=2, padx=20, pady=20, sticky=N)
        self.flowspin.grid(column=1, row=3, padx=20, pady=20, sticky=N)
        self.overspin.grid(column=2, row=3, padx=20, pady=20, sticky=N)
        self.displbl.grid(column=3, row=3, padx=20, pady=20, sticky=N)
        backbtn.grid(column=1, row=9, columnspan=4, padx=20, pady=10, sticky=S+E)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, minsize=10)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(10, minsize=10)

    def _flowrate_change(self, oldval, newval):
        self.feed.flowrate = newval

    def _overage_change(self, oldval, newval):
        self.feed.pulse_overage = newval

    def _pour_mode(self):
        self.dutyspin.config(state=DISABLED)
        self.amntspin.config(state=DISABLED)
        self.flowspin.config(state=DISABLED)
        self.overspin.config(state=DISABLED)
        self.pourbtn.config(text="Cancel")
        self.dispensing = True

    def _conf_mode(self):
        self.dutyspin.config(state=NORMAL)
        self.amntspin.config(state=NORMAL)
        self.flowspin.config(state=NORMAL)
        self.overspin.config(state=NORMAL)
        self.pourbtn.config(text="Pour")
        self.dispensing = False
        self._cancel_feed()

    def _cancel_feed(self):
        if self.feed.isFlowing():
            self.feed.stopFeed()
        if self.start_pid:
            self.after_cancel(self.start_pid)
            self.start_pid = None
        if self.stop_pid:
            self.after_cancel(self.stop_pid)
            self.stop_pid = None

    def handle_button_pour(self):
        if self.dispensing:
            # Cancel button pressed
            self._conf_mode()
        else:
            # Pour button pressed
            self._pour_mode()
            self.dispensed = 0.0
            self.target_ml = self.amntspin.get()
            self.duty_cycle = self.dutyspin.get() / 100.0
            self._feed_cycle_start()

    def _feed_cycle_start(self):
        self.start_pid = None
        if self.dispensed >= self.target_ml - 0.05:
            self._conf_mode()
            return
        self.start_pid = self.after(1001, self._feed_cycle_start)
        remaining_ml = self.target_ml - self.dispensed
        remtime = remaining_ml / self.feed.flowrate
        stop_ms = int(max(0.01,min(remtime, self.duty_cycle))*1000)
        self.stop_pid = self.after(stop_ms, self._feed_cycle_stop, stop_ms)
        if self.duty_cycle < 1.0 or self.dispensed == 0.0:
            self.feed.startFeed()
        self.displbl.config(text="Dispensed:\n%.1f ml (%d%%)" % (self.dispensed, int(100*self.dispensed/self.target_ml+0.5)))

    def _feed_cycle_stop(self, ms):
        self.dispensed += self.feed.flowrate * (ms / 1000.0)
        self.dispensed += self.feed.pulse_overage
        if self.duty_cycle < 1.0 or self.dispensed >= self.target_ml - 0.05:
            self.feed.stopFeed()
        self.displbl.config(text="Dispensed:\n%.1f ml (%d%%)" % (self.dispensed, int(100*self.dispensed/self.target_ml+0.5)))

    def handle_button_back(self):
        if self.feed.isFlowing():
            self.feed.stopFeed()
        self.feed.flowrate = self.flowspin.get()
        self.feed.pulse_overage = self.overspin.get()
        self.master.save_configs()
        self.master.screen_pop()

