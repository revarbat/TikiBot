"""
This is the library for the Adafruit Motor Shield V2 for Arduino.
It supports DC motors & Stepper motors with microstepping as well
as stacking-support. It is *not* compatible with the V1 library!
It will only work with https://www.adafruit.com/products/1483

Adafruit invests time and resources providing this open
source code, please support Adafruit and open-source hardware
by purchasing products from Adafruit!

BSD license, check license.txt for more information.
All text above must be included in any redistribution.
"""

from Adafruit_PCA9685 import PCA9685
import time



MICROSTEPS = 16  # 8 or 16

MOTOR1_A = 2
MOTOR1_B = 3
MOTOR2_A = 1
MOTOR2_B = 4
MOTOR4_A = 0
MOTOR4_B = 6
MOTOR3_A = 5
MOTOR3_B = 7

LOW = 0
HIGH = 1

FORWARD = 1
BACKWARD = 2
BRAKE = 3
RELEASE = 4

SINGLE = 1
DOUBLE = 2
INTERLEAVE = 3
MICROSTEP = 4


if MICROSTEPS == 8:
    microstepcurve = [0, 50, 98, 142, 180, 212, 236, 250, 255]
elif MICROSTEPS == 16:
    microstepcurve = [0, 25, 50, 74, 98, 120, 141, 162, 180, 197, 212, 225, 236, 244, 250, 253, 255]



class Adafruit_DCMotor(object):
    def __init__(self, shield, num, pwmpin, in1pin, in2pin):
        self.PWMpin = pwmpin
        self.IN1pin = in1pin
        self.IN2pin = in2pin
        self.motornum = num
        self.motor_shield = shield

    def run(self, cmd):
        if cmd == FORWARD:
            self.motor_shield.setPin(self.IN2pin, LOW)  # take low first to avoid 'break'
            self.motor_shield.setPin(self.IN1pin, HIGH)
        if cmd == BACKWARD:
            self.motor_shield.setPin(self.IN1pin, LOW)  # take low first to avoid 'break'
            self.motor_shield.setPin(self.IN2pin, HIGH)
        if cmd == RELEASE:
            self.motor_shield.setPin(self.IN1pin, LOW)
            self.motor_shield.setPin(self.IN2pin, LOW)

    def setSpeed(self, speed):
        self.motor_shield.setPWM(self.PWMpin, speed*16)


class Adafruit_StepperMotor(object):
    def __init__(self, shield, num, steps, pwma, pwmb, ain1, bin1, ain2, bin2):
        self.usperstep = 0
        self.PWMApin = pwma
        self.AIN1pin = ain1
        self.AIN2pin = ain2
        self.PWMBpin = pwmb
        self.BIN1pin = bin1
        self.BIN2pin = bin2
        self.revsteps = steps  # steps per revolution
        self.currentstep = 0
        self.steppernum = num
        self.motor_shield = shield

    def setSpeed(self, rpm):
        self.usperstep = 60000000 / (revsteps * rpm)

    def release(self):
        self.motor_shield.setPin(self.AIN1pin, LOW)
        self.motor_shield.setPin(self.AIN2pin, LOW)
        self.motor_shield.setPin(self.BIN1pin, LOW)
        self.motor_shield.setPin(self.BIN2pin, LOW)
        self.motor_shield.setPWM(self.PWMApin, 0)
        self.motor_shield.setPWM(self.PWMBpin, 0)

    def step(self, steps, dir, style=SINGLE):
        uspers = usperstep
        ret = 0
        if style == INTERLEAVE:
            uspers /= 2
        elif style == MICROSTEP:
            uspers /= MICROSTEPS
            steps *= MICROSTEPS
        while steps:
            steps -= 1
            ret = self.onestep(dir, style)
            time.sleep(uspers/1000000.0)

    def onestep(self, dir, style):
        ocra = 255
        ocrb = 255
        # determine what sort of stepping procedure we're up to
        if style == SINGLE:
            if (self.currentstep/(MICROSTEPS/2)) % 2 != 0:
                # we're at an odd step, weird
                if dir == FORWARD:
                    self.currentstep += MICROSTEPS/2
                else:
                    self.currentstep -= MICROSTEPS/2
            else:
                # go to the next even step
                if dir == FORWARD:
                    self.currentstep += MICROSTEPS
                else:
                    self.currentstep -= MICROSTEPS
        elif style == DOUBLE:
            if (self.currentstep/(MICROSTEPS/2)) % 2 == 0:
                # we're at an even step, weird
                if dir == FORWARD:
                    self.currentstep += MICROSTEPS/2
                else:
                    self.currentstep -= MICROSTEPS/2
            else:
                # go to the next odd step
                if dir == FORWARD:
                    self.currentstep += MICROSTEPS
                else:
                    self.currentstep -= MICROSTEPS
        elif style == INTERLEAVE:
            if dir == FORWARD:
                self.currentstep += MICROSTEPS/2
            else:
                self.currentstep -= MICROSTEPS/2
        elif style == MICROSTEP:
            if dir == FORWARD:
                self.currentstep += 1
            else:
                self.currentstep -= 1
            self.currentstep += MICROSTEPS*4
            self.currentstep %= MICROSTEPS*4
            ocra = 0
            ocrb = 0
            if self.currentstep >= 0 and self.currentstep < MICROSTEPS:
                ocra = microstepcurve[MICROSTEPS - self.currentstep]
                ocrb = microstepcurve[self.currentstep]
            elif self.currentstep >= MICROSTEPS and self.currentstep < MICROSTEPS*2:
                ocra = microstepcurve[self.currentstep - MICROSTEPS]
                ocrb = microstepcurve[MICROSTEPS*2 - self.currentstep]
            elif self.currentstep >= MICROSTEPS*2 and self.currentstep < MICROSTEPS*3:
                ocra = microstepcurve[MICROSTEPS*3 - self.currentstep]
                ocrb = microstepcurve[self.currentstep - MICROSTEPS*2]
            elif self.currentstep >= MICROSTEPS*3 and self.currentstep < MICROSTEPS*4:
                ocra = microstepcurve[self.currentstep - MICROSTEPS*3]
                ocrb = microstepcurve[MICROSTEPS*4 - self.currentstep]

        self.currentstep += MICROSTEPS*4
        self.currentstep %= MICROSTEPS*4
        self.motor_shield.setPWM(self.PWMApin, ocra*16)
        self.motor_shield.setPWM(self.PWMBpin, ocrb*16)

        latch_state = 0
        if style == MICROSTEP:
            if self.currentstep >= 0 and self.currentstep < MICROSTEPS:
                latch_state |= 0x03
            if self.currentstep >= MICROSTEPS and self.currentstep < MICROSTEPS*2:
                latch_state |= 0x06
            if self.currentstep >= MICROSTEPS*2 and self.currentstep < MICROSTEPS*3:
                latch_state |= 0x0C
            if self.currentstep >= MICROSTEPS*3 and self.currentstep < MICROSTEPS*4:
                latch_state |= 0x09
        else:
            phase = self.currentstep/(MICROSTEPS/2)
            if phase == 0:
                latch_state |= 0x1 # energize coil 1 only
            elif phase == 1:
                latch_state |= 0x3 # energize coil 1+2
            elif phase == 2:
                latch_state |= 0x2 # energize coil 2 only
            elif phase == 3:
                latch_state |= 0x6 # energize coil 2+3
            elif phase == 4:
                latch_state |= 0x4 # energize coil 3 only
            elif phase == 5:
                latch_state |= 0xC # energize coil 3+4
            elif phase == 6:
                latch_state |= 0x8 # energize coil 4 only
            elif phase == 7:
                latch_state |= 0x9 # energize coil 1+4
        self.motor_shield.setPin(self.AIN2pin, HIGH if latch_state & 0x1 else LOW)
        self.motor_shield.setPin(self.BIN1pin, HIGH if latch_state & 0x2 else LOW)
        self.motor_shield.setPin(self.AIN1pin, HIGH if latch_state & 0x4 else LOW)
        self.motor_shield.setPin(self.BIN2pin, HIGH if latch_state & 0x8 else LOW)
        return self.currentstep


class Adafruit_MotorShield(object):
    def __init__(self, address=0x60, **kwargs):
        self._address = address
        self._freq = 1600
        self.dcmotors = [None, None, None, None]
        self.steppers = [None, None]
        self._pwm = PCA9685(address, **kwargs)

    def begin(self, freq=1600):
        self._freq = freq
        self._pwm.set_pwm_freq(self._freq)
        for i in range(16):
            self._pwm.set_pwm(i, 0, 0)

    def setPWM(self, pin, value):
        if value > 4095:
            self._pwm.set_pwm(pin, 4096, 0)
        else:
            self._pwm.set_pwm(pin, 0, value)

    def setPin(self, pin, value):
        if value == LOW:
            self._pwm.set_pwm(pin, 0, 0)
        else:
            self._pwm.set_pwm(pin, 4096, 0)

    def getMotor(self, num):
        if num < 1 or num > 4:
            return None
        num -= 1
        if self.dcmotors[num] == None:
            # not init'd yet!
            if num == 0:
                pwm = 8
                in2 = 9
                in1 = 10
            elif num == 1:
                pwm = 13
                in2 = 12
                in1 = 11
            elif num == 2:
                pwm = 2
                in2 = 3
                in1 = 4
            elif num == 3:
                pwm = 7
                in2 = 6
                in1 = 5
            self.dcmotors[num] = Adafruit_DCMotor(self, num, pwm, in1, in2)
        return self.dcmotors[num]

    def getStepper(self, steps, num):
        if num < 1 or num > 2:
            return None
        num -= 1
        if self.steppers[num] == None:
            # not init'd yet!
            if num == 0:
                pwma = 8
                ain2 = 9
                ain1 = 10
                pwmb = 13
                bin2 = 12
                bin1 = 11
            elif num == 1:
                pwma = 2
                ain2 = 3
                ain1 = 4
                pwmb = 7
                bin2 = 6
                bin1 = 5
            self.steppers[num] = Adafruit_StepperMotor(self, num, steps, pwma, pwmb, ain1, bin1, ain2, bin2)
        return self.steppers[num]

