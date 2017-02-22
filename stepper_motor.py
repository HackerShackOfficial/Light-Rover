import RPi.GPIO as GPIO
import time
import threading


# TODO: add acceleration
class Stepper(object):

    def __init__(self, a1, a2, b1, b2, steps=50.0, rpm=30.0):

        self.rpm = rpm
        self.steps_per_rev = steps
        self.current_step = 0

        self.coil_A_1_pin = a1
        self.coil_A_2_pin = a2
        self.coil_B_1_pin = b1
        self.coil_B_2_pin = b2

        GPIO.setup(a1, GPIO.OUT)
        GPIO.setup(a2, GPIO.OUT)
        GPIO.setup(b1, GPIO.OUT)
        GPIO.setup(b2, GPIO.OUT)

        self.set_step(0, 0, 0, 0)

    def forward(self, steps, delay=None, rpm=None, hold_position=True):
        self.current_step = 0
        d = delay if delay else self.get_delay(rpm)

        for step in range(0, steps):
            self.set_step(1, 0, 1, 0)
            time.sleep(d)
            self.set_step(0, 1, 1, 0)
            time.sleep(d)
            self.set_step(0, 1, 0, 1)
            time.sleep(d)
            self.set_step(1, 0, 0, 1)
            time.sleep(d)

        if hold_position is False:
            self.set_step(0, 0, 0, 0)

    def backwards(self, steps, delay=None, rpm=None, hold_position=True):
        self.current_step = 0
        d = delay if delay else self.get_delay(rpm)

        for step in range(0, steps):
            self.set_step(1, 0, 0, 1)
            time.sleep(d)
            self.set_step(0, 1, 0, 1)
            time.sleep(d)
            self.set_step(0, 1, 1, 0)
            time.sleep(d)
            self.set_step(1, 0, 1, 0)
            time.sleep(d)

        if hold_position is False:
            self.set_step(0, 0, 0, 0)

    def set_rpm(self, rpm):
        self.rpm = rpm

    def microstep(self, steps, delay=None, rpm=None, hold_position=True):
        d = delay if delay else self.get_delay(rpm)
        steps_left = abs(steps)

        while steps_left > 0:
            if steps > 0:  # forward
                self.current_step += 1
                if self.current_step == self.steps_per_rev*4:
                    self.current_step = 0
            else:  # backwards
                if self.current_step == 0:
                    self.current_step = self.steps_per_rev*4
                self.current_step -= 1

            steps_left -= 1
            self.step_sequence(self.current_step % 4)
            time.sleep(d)

        if hold_position is False:
            self.set_step(0, 0, 0, 0)
            self.current_step = 0

    def step_sequence(self, num):
        if num == 0:
            self.set_step(1, 0, 0, 1)
        elif num == 1:
            self.set_step(0, 1, 0, 1)
        elif num == 2:
            self.set_step(0, 1, 1, 0)
        else:
            self.set_step(1, 0, 1, 0)

    def set_step(self, w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def get_delay(self, rpm=None):
        local_rpm = rpm if rpm else self.rpm
        return 60.0 * 1000.0 / local_rpm / (self.steps_per_rev * 4.0) / 1000.0

    def cleanup(self):
        self.set_step(0, 0, 0, 0)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    stepper1 = Stepper(2, 3, 4, 17)
    stepper2 = Stepper(27, 22, 10, 9)

    while True:
        steps_f = raw_input("How many steps forward? ")
        st1 = threading.Thread(target=stepper2.forward, args=(int(steps_f),))
        st2 = threading.Thread(target=stepper1.backwards, args=(int(steps_f),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

        steps_b = raw_input("How many steps backwards? ")
        st1 = threading.Thread(target=stepper2.backwards, args=(int(steps_b),))
        st2 = threading.Thread(target=stepper1.forward, args=(int(steps_b),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()
