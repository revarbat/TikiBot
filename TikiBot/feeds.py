import sys
import time
import yaml
import platform
import operator

from Adafruit_MotorHAT import Adafruit_MotorHAT as AFMH
from Adafruit_GPIO.I2C import get_i2c_device


progstart_time = time.time()


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class SupplyFeed(object):
    motor_controllers = {}
    dc_motors = {}
    max_motor_num = 0
    feed_order = []
    feeds = {}
    feed_types = {}

    def __init__(self, type_, name, flowrate=14.2, overage=0.25, avail=True):
        if type_ not in SupplyFeed.feed_types:
            SupplyFeed.feed_types[type_] = []
        SupplyFeed.feed_types[type_].append(self)
        self.type_ = type_
        self.name = name
        self.flowrate = flowrate
        self.pulse_overage = overage
        self.flowing = False
        self.avail = avail
        self.motor_num = SupplyFeed.max_motor_num
        self.motor = None  # Defer instantiation for X-platform debugging
        SupplyFeed.max_motor_num += 1
        SupplyFeed.feeds[name] = self
        SupplyFeed.feed_order.append(self)

    @classmethod
    def fromDict(cls, d):
        """Create a new SupplyFeed instance from a dictionary description."""
        return cls(d['type'], d['name'], d['flowrate'], d.get('overage', 0.25), d['available'])

    def toDict(self):
        """Create a dictionary description of this SupplyFeed instance."""
        return {
            'type': self.type_,
            'name': self.name,
            'flowrate': self.flowrate,
            'overage': self.pulse_overage,
            'available': self.avail,
        }

    @classmethod
    def load(cls, stream):
        """Load SupplyFeeds from given YAML data"""
        dictarr = yaml.load(stream)
        for d in dictarr:
            cls.fromDict(d)

    @classmethod
    def dump(cls):
        """Create a YAML dump of all SupplyFeeds"""
        return yaml.dump([feed.toDict() for feed in cls.feed_order])

    @classmethod
    def _getMotorByNumber(cls, motor_num):
        """Returns the DCMotor instance for the given motor number."""
        addr = 0x60 + motor_num // 4
        num = motor_num % 4
        if addr not in cls.motor_controllers:
            busnum = 0
            if platform.system() == "Linux":
                if "udooneo" in platform.release():
                    busnum = 1
            cls.motor_controllers[addr] = AFMH(addr, i2c_bus=busnum)
        if motor_num not in cls.dc_motors:
            cls.dc_motors[motor_num] = cls.motor_controllers[addr].getMotor(num + 1)
        return cls.dc_motors[motor_num]

    @classmethod
    def getTypeNames(cls):
        """Returns a sorted string list of all SupplyFeed types."""
        return sorted(cls.feed_types.keys())

    @classmethod
    def getFeedsByType(cls, name):
        """Returns a list of all SupplyFeeds of a given type, sorted by name."""
        feed_list = cls.feed_types[name]
        return sorted(feed_list, key=operator.attrgetter('name'))

    @classmethod
    def getNames(cls):
        """Returns a sorted list of the names of all SupplyFeeds."""
        return sorted(cls.feeds.keys())

    @classmethod
    def getAll(cls):
        """Returns a list of all SupplyFeeds, sorted by name."""
        for key in sorted(cls.feeds.keys()):
            yield cls.feeds[key]

    @classmethod
    def getAllOrdered(cls):
        """Returns a list of all SupplyFeeds, sorted by feed number."""
        return cls.feed_order

    @classmethod
    def getByName(cls, name):
        """Get a SupplyFeed instance by name."""
        return cls.feeds[name]

    def getName(self):
        """Get the name of this SupplyFeed instance."""
        return self.name

    def isFlowing(self):
        """Returns true if this SupplyFeed if currently on/flowing."""
        return self.flowing

    def startFeed(self):
        """Turn on this SupplyFeed, to start it flowing."""
        if platform.system() == "Linux":
            # turn on solonoid/motor for feed
            if self.motor is None:
                self.motor = SupplyFeed._getMotorByNumber(self.motor_num)
            self.motor.setSpeed(255)
            self.motor.run(AFMH.FORWARD)
            self.flowing = True
        else:
            eprint("Starting feed %d @%f" % (self.motor_num, time.time() - progstart_time))

    def stopFeed(self):
        """Turn off this SupplyFeed, to stop it's flow."""
        if platform.system() == "Linux":
            # turn off solonoid/motor for feed
            if self.motor is None:
                self.motor = SupplyFeed._getMotorByNumber(self.motor_num)
            self.motor.setSpeed(0)
            self.motor.run(AFMH.RELEASE)
            self.flowing = False
        else:
            eprint("STOPPING feed %d @%f" % (self.motor_num, time.time() - progstart_time))

    def delete_feed(self):
        """Delete this SupplyFeed, removing it from the feed_order, feeds, and feed_types"""
        del SupplyFeed.feeds[self.name]
        SupplyFeed.feed_types[self.type_].remove(self)
        if not SupplyFeed.feed_types[self.type_]:
            del SupplyFeed.feed_types[self.type_]
        SupplyFeed.feed_order.remove(self)
        SupplyFeed.max_motor_num -= 1

    def rename(self, newname):
        """Change the name of this SupplyFeed."""
        del SupplyFeed.feeds[self.name]
        self.name = newname
        SupplyFeed.feeds[newname] = self

    def retype(self, newtype):
        """Change the type of this SupplyFeed."""
        SupplyFeed.feed_types[self.type_].remove(self)
        if not SupplyFeed.feed_types[self.type_]:
            del SupplyFeed.feed_types[self.type_]
        self.type_ = newtype
        if newtype not in SupplyFeed.feed_types:
            SupplyFeed.feed_types[newtype] = []
        SupplyFeed.feed_types[newtype].append(self)

    @classmethod
    def transpose(cls, pos):
        """Transpose the given feed with the one after it in the feed order, swapping their motor_num's."""
        if pos >= 0 and pos < len(cls.feed_order)-1:
            cls.feed_order[pos:pos+2] = reversed(cls.feed_order[pos:pos+2])
            for n, feed in enumerate(cls.feed_order):
                feed.motor_num = n

    def getOrder(self):
        """Returns the ordinal position of this feed in the feed order.  0-based."""
        return SupplyFeed.feed_order.index(self)

    def reorderUp(self):
        """Moves the current SupplyFeed towards the front of the feed_order ordering."""
        idx = self.getOrder()
        SupplyFeed.transpose(idx-1)

    def reorderDown(self):
        """Moves the current SupplyFeed towards the end of the feed_order ordering."""
        idx = self.getOrder()
        SupplyFeed.transpose(idx)


