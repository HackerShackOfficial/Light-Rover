import time
import math
import sys
import numpy as np
import threading
import signal
import RPi.GPIO as GPIO
from vector_drawings import *
from neopixel import *
from PIL import Image, ImageEnhance
from stepper_motor import Stepper
"""
Paints an light picture of an image by sectioning chunks to display on a led matrix.
Starts at the upper left hand corner of the image.

"""


class LightRover(object):

    def __init__(self, left_wheel_stepper, right_wheel_stepper, led_matrix):
        if not left_wheel_stepper or not right_wheel_stepper or not led_matrix:
            raise ValueError("Please make sure all parameters are defined!")

        self.s1 = left_wheel_stepper
        self.s2 = right_wheel_stepper
        self.matrix = led_matrix
        self.degree_step_coefficient = 1.45

    def paint_image(self, image_file):
        """
        Paints the image by traversing from the upper left corner to the bottom right/left
        :param image_file:
        :return:
        """
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
                LightRover.clear_matrix(self.matrix)

                # Move to the next space
                self.move_forward(90)

            # Go to the next row Todo: parameterize
            if is_even_row:
                self.turn_degrees_right(90)
                self.move_forward(125)
                self.turn_degrees_right(90)
                self.move_forward(90)
            else:
                self.turn_degrees_left(90)
                self.move_forward(125)
                self.turn_degrees_left(90)
                self.move_forward(90)

    def paint_vector(self, vector_arr, single_value_affects_pixels=None, pixel_has_pos=False):
        """
        :param vector_arr: array of light vector objects
        :param single_value_affects_pixels: array of pixel indexes to change if one value RGB value is provided
        :param pixel_has_pos: True if using LightPixels instead of a 2D array of values
        :return:
        """

        for vector in vector_arr:
            if not isinstance(vector, LightVector):
                raise ValueError("Vector array must contain only light vectors!")

            if pixel_has_pos is True:
                for pixel in vector.pixel_data:
                    self.matrix.setPixelColor(pixel.pos, pixel.r, pixel.g, pixel.b)
            elif len(vector.pixel_data) == 1 and single_value_affects_pixels is not None:
                pixels = self.__create_pixel_array(vector.pixel_data[0], single_value_affects_pixels)
                self.show_pixels(pixels)
            else:
                self.show_pixels(vector.pixel_data)

            self.move_forward(vector.steps)
            LightRover.clear_matrix(self.matrix)

            if vector.angle < 0:
                self.turn_degrees_left(vector.angle)
            else:
                self.turn_degrees_right(vector.angle)

    def __create_pixel_array(self, value, affected_values):
        """
        Creates an array of pixel which are the size of the matrix. 'affected_values' indexes are given
        the color of 'value'
        :param value:
        :param affected_values:
        :return:
        """
        pixel_arr = []

        if self.matrix is None:
            return []

        for pixel in range(self.matrix.numPixels()):
            pixel_arr.append([0, 0, 0])

        for pixel in affected_values:
            pixel_arr[pixel] = value

        return pixel_arr

    def move_forward(self, steps):
        st1 = threading.Thread(target=self.s1.microstep_forward, args=(int(steps),))
        st2 = threading.Thread(target=self.s2.microstep_backward, args=(int(steps),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

    def move_backward(self, steps):
        st1 = threading.Thread(target=self.s1.microstep_backward, args=(int(steps),))
        st2 = threading.Thread(target=self.s2.microstep_forward, args=(int(steps),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

    def turn_degrees_right(self, angle):
        self.turn_right(abs(self.degree_step_coefficient * angle))

    def turn_right(self, steps):
        st1 = threading.Thread(target=self.s1.microstep_forward, args=(int(steps),))
        st2 = threading.Thread(target=self.s2.microstep_forward, args=(int(steps),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

    def turn_degrees_left(self, angle):
        self.turn_left(abs(self.degree_step_coefficient * angle))

    def turn_left(self, steps):
        st1 = threading.Thread(target=self.s1.microstep_backward, args=(int(steps),))
        st2 = threading.Thread(target=self.s2.microstep_backward, args=(int(steps),))
        st1.start()
        st2.start()
        st1.join()
        st2.join()

    def show_pixels(self, values):
        """
        :param values: an array of values to display on the led matrix
        :return:
        """
        for pixel in range(len(values)):
            # r and g are swapped for some reason
            self.matrix.setPixelColor(pixel, Color(values[pixel][1], values[pixel][0], values[pixel][2]))
        self.matrix.show()

    @staticmethod
    def clear_matrix(matrix):
        for p in range(matrix.numPixels()):
            matrix.setPixelColor(p, Color(0, 0, 0))
        matrix.show()


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
    LightRover.clear_matrix(led_matrix)
    stepper1.cleanup()
    stepper2.cleanup()
    GPIO.cleanup()
    sys.exit(0)


def signal_handler(signal, frame):
    cleanup()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    imageFile = None
    if len(sys.argv) >= 2:
        imageFile = sys.argv[1]

    GPIO.setmode(GPIO.BCM)

    stepper1 = Stepper(2, 3, 4, 17)
    stepper2 = Stepper(27, 22, 10, 9)

    stepper1.set_rpm(60.0)
    stepper2.set_rpm(60.0)

    led_matrix = create_strip(64)
    led_matrix.begin()

    rover = LightRover(stepper1, stepper2, led_matrix)

    # Image
    '''
    if imageFile:
        rover.paint_image(imageFile)
    else:
        print "No image file provided!"
        exit(1)
    '''

    # Vector
    rover.paint_vector(dog, single_value_affects_pixels=[27, 28, 35, 36])

    cleanup()

