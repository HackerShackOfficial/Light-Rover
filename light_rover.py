import time
import math
import sys
import numpy as np
import threading
import signal
import RPi.GPIO as GPIO
from neopixel import *
from PIL import Image, ImageEnhance
from stepper_motor import Stepper
"""
Paints an light picture of an image by sectioning chunks to display on a led matrix.
Starts at the upper left hand corner of the image.

This file is a work in progress. Will refactor once tuned properly.
"""


class LightRover(object):

    def __init__(self, left_wheel_stepper, right_wheel_stepper, led_matrix):
        if not left_wheel_stepper or not right_wheel_stepper or not led_matrix:
            raise ValueError("Please make sure all parameters are defined!")

        self.s1 = left_wheel_stepper
        self.s2 = right_wheel_stepper
        self.matrix = led_matrix

    def paint_image(self, image_file):
        print "Converting: %s" % image_file

        image = Image.open(image_file)
        converter = ImageEnhance.Color(image)
        image = converter.enhance(2)
        pixels = image.load()

        im_width, im_height = image.size

        chunk_size = int(math.sqrt(self.matrix.numPixels()))
        num_chunks_w = int(math.ceil(im_width / float(chunk_size)))
        num_chunks_h = int(math.ceil(im_height / float(chunk_size)))

        for h_chunk in range(num_chunks_h):
            is_even_row = (h_chunk % 2) == 0
            w_chunk_range = range(num_chunks_w) if is_even_row else range(num_chunks_w - 1, -1, -1)
            w_range = range(chunk_size) if is_even_row else range(chunk_size - 1, -1, -1)
            h_range = range(chunk_size) if is_even_row else range(chunk_size - 1, -1, -1)

            for w_chunk in w_chunk_range:
                index = 0
                pixel_buffer = np.zeros((math.pow(chunk_size, 2), 3), dtype=np.int)
                for h in h_range:
                    for w in w_range:
                        try:
                            pixel_buffer[index][0] = int(pixels[w + chunk_size * w_chunk, h + chunk_size * h_chunk][0])
                            pixel_buffer[index][1] = int(pixels[w + chunk_size * w_chunk, h + chunk_size * h_chunk][1])
                            pixel_buffer[index][2] = int(pixels[w + chunk_size * w_chunk, h + chunk_size * h_chunk][2])
                        except IndexError:
                            pass  # pixels should be black
                        index += 1

                # show pixel data, sleep for 1 second then clear
                self.show_pixels(pixel_buffer.tolist())
                time.sleep(1)
                self.clear_matrix()

                # Move to the next space
                self.move_forward(25)

            # Go to the next row
            if is_even_row:
                self.turn_right(35)
                self.move_forward(35)
                self.turn_right(35)
                self.move_forward(25)
            else:
                self.turn_left(32)
                self.move_forward(35)
                self.turn_left(32)
                self.move_forward(25)

    def paint_vector(self, vector):
        pass

    def move_forward(self, steps):
        st1 = threading.Thread(target=self.s1.forward, args=(int(steps),))
        st2 = threading.Thread(target=self.s2.backwards, args=(int(steps),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

    def move_backward(self, steps):
        st1 = threading.Thread(target=self.s1.backwards, args=(int(steps),))
        st2 = threading.Thread(target=self.s2.forward, args=(int(steps),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

    def turn_right(self, steps):
        st1 = threading.Thread(target=self.s1.forward, args=(int(steps),))
        st2 = threading.Thread(target=self.s2.forward, args=(int(steps),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

    def turn_left(self, steps):
        st1 = threading.Thread(target=self.s1.backwards, args=(int(steps),))
        st2 = threading.Thread(target=self.s2.backwards, args=(int(steps),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

    def show_pixels(self, values):
        for pixel in range(len(values)):
            self.matrix.setPixelColor(pixel, Color(values[pixel][0], values[pixel][1], values[pixel][2]))
        self.matrix.show()

    def clear_matrix(self):
        for p in range(self.matrix.numPixels()):
            self.matrix.setPixelColor(p, Color(0, 0, 0))
        self.matrix.show()


# #### HELPER METHODS #### #

def create_strip(leds, led_pin=18, led_freq_hz=800000, led_dma=5, led_brightness=10, led_invert=False):
    """
    :param leds:
    :param led_pin:
    :param led_freq_hz:
    :param led_dma:
    :param led_brightness:
    :param led_invert:
    :return:

    # LED strip configuration:
    LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 5  # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    """

    return Adafruit_NeoPixel(leds, led_pin, led_freq_hz, led_dma, led_invert, led_brightness)


def cleanup():
    stepper1.cleanup()
    stepper2.cleanup()
    GPIO.cleanup()
    sys.exit(0)


def signal_handler(signal, frame):
    cleanup()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    if len(sys.argv) < 2:
        print "No input image given. Make sure you specify a valid input image."
        exit(0)

    imageFile = sys.argv[1]

    GPIO.setmode(GPIO.BCM)

    stepper1 = Stepper(27, 22, 10, 9)
    stepper2 = Stepper(2, 3, 4, 17)

    stepper1.set_rpm(60.0)
    stepper2.set_rpm(60.0)

    led_matrix = create_strip(64)
    led_matrix.begin()

    rover = LightRover(stepper1, stepper2, led_matrix)
    rover.paint_image(imageFile)
    cleanup()

