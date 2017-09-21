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
        SupplyFeed.feed_types[type_].append(type_)
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
        return cls(d['type'], d['name'], d['flowrate'], d.get('overage', 0.25), d['available'])

    def toDict(self):
        return {
            'type': self.type_,
            'name': self.name,
            'flowrate': self.flowrate,
            'overage': self.pulse_overage,
            'available': self.avail,
        }

    @classmethod
    def load(cls, stream):
        dictarr = yaml.load(stream)
        for d in dictarr:
            cls.fromDict(d)

    @classmethod
    def dump(cls):
        return yaml.dump([feed.toDict() for feed in cls.feed_order])

    @classmethod
    def getMotorByNumber(cls, motor_num):
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
        return sorted(cls.feed_types.keys())

    @classmethod
    def getFeedsByType(cls, name):
        feed_list = cls.feed_types[name]
        return sorted(feed_list, key=operator.attrgetter('name'))

    @classmethod
    def getNames(cls):
        return sorted(cls.feeds.keys())

    @classmethod
    def getAll(cls):
        for key in sorted(cls.feeds.keys()):
            yield cls.feeds[key]

    @classmethod
    def getByName(cls, name):
        return cls.feeds[name]

    def getName(self):
        return self.name

    def rename(self, newname):
        del SupplyFeed.feeds[self.name]
        self.name = newname
        SupplyFeed.feeds[newname] = self

    def isFlowing(self):
        return self.flowing

    def startFeed(self):
        if platform.system() == "Linux":
            # turn on solonoid/motor for feed
            if self.motor is None:
                self.motor = SupplyFeed.getMotorByNumber(self.motor_num)
            self.motor.setSpeed(255)
            self.motor.run(AFMH.FORWARD)
            self.flowing = True
        else:
            eprint("Starting feed %d @%f" % (self.motor_num, time.time() - progstart_time))

    def stopFeed(self):
        if platform.system() == "Linux":
            # turn off solonoid/motor for feed
            if self.motor is None:
                self.motor = SupplyFeed.getMotorByNumber(self.motor_num)
            self.motor.setSpeed(0)
            self.motor.run(AFMH.RELEASE)
            self.flowing = False
        else:
            eprint("STOPPING feed %d @%f" % (self.motor_num, time.time() - progstart_time))


