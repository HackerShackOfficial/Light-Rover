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


# TODO: move methods into this class
class LightRover(object):

    def __init__(self, left_wheel_stepper, right_wheel_stepper, led_matrix):
        pass

    def paint_image(self, filename):
        pass

    def paint_vector(self, vector):
        pass


GPIO.setmode(GPIO.BCM)

stepper1 = Stepper(27, 22, 10, 9)
stepper2 = Stepper(2, 3, 4, 17)

stepper1.set_rpm(60.0)
stepper2.set_rpm(60.0)


def signal_handler(signal, frame):
    stepper1.cleanup()
    stepper2.cleanup()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def move_forward(s1, s2, steps):
    st1 = threading.Thread(target=s1.forward, args=(int(steps),))
    st2 = threading.Thread(target=s2.backwards, args=(int(steps),))
    st1.start()
    st2.start()
    st1.join()
    st2.join()


def turn_right(s1, s2, steps):
    st1 = threading.Thread(target=s1.forward, args=(int(steps),))
    st2 = threading.Thread(target=s2.forward, args=(int(steps),))
    st1.start()
    st2.start()
    st1.join()
    st2.join()


def turn_left(s1, s2, steps):
    st1 = threading.Thread(target=s1.backwards, args=(int(steps),))
    st2 = threading.Thread(target=s2.backwards, args=(int(steps),))
    st1.start()
    st2.start()
    st1.join()
    st2.join()


def create_strip(leds):
    # LED strip configuration:
    LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 5  # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

    return Adafruit_NeoPixel(leds, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)


def clear_strip(strip):
    for p in range(strip.numPixels()):
        strip.setPixelColor(p, Color(0, 0, 0))
    strip.show()


if len(sys.argv) < 2:
    print "No input image given. Make sure you specify a valid input image."
    exit(0)

imageFile = sys.argv[1]

print "Converting: %s" % imageFile

image = Image.open(imageFile)
converter = ImageEnhance.Color(image)
image = converter.enhance(2)
pixels = image.load()

chunkSize = 8
strip = create_strip(int(math.pow(chunkSize, 2)))
strip.begin()

width, height = image.size

numChunksW = int(math.ceil(width/float(chunkSize)))
numChunksH = int(math.ceil(height/float(chunkSize)))

for hChunk in range(numChunksH):
    wChunkRange = range(numChunksW)
    wRange = range(chunkSize)
    hRange = range(chunkSize)
    turnRight = True
    if hChunk % 2:  # odd (backwards)
        wChunkRange = range(numChunksW - 1, -1, -1)
        wRange = range(chunkSize - 1, -1, -1)
        hRange = range(chunkSize - 1, -1, -1)
        turnRight = False

    for wChunk in wChunkRange:
        pixelBuffer = np.zeros((math.pow(chunkSize, 2), 3), dtype=np.int)
        index = 0
        for h in hRange:
            for w in wRange:
                try:
                    pixelBuffer[index][0] = int(pixels[w + chunkSize * wChunk, h + chunkSize * hChunk][0])
                    pixelBuffer[index][1] = int(pixels[w + chunkSize * wChunk, h + chunkSize * hChunk][1])
                    pixelBuffer[index][2] = int(pixels[w + chunkSize * wChunk, h + chunkSize * hChunk][2])
                except IndexError:
                    pass  # pixels should be black
                index += 1

        pBL = pixelBuffer.tolist()
        for pixel in range(len(pBL)):
            strip.setPixelColor(pixel, Color(pBL[pixel][0], pBL[pixel][1], pBL[pixel][2]))

        strip.show()
        time.sleep(1)
        clear_strip(strip)

        # Move to the next space
        move_forward(stepper1, stepper2, 25)

    # Go to the next row
    if turnRight:
        turn_right(stepper1, stepper2, 35)
        move_forward(stepper1, stepper2, 35)
        turn_right(stepper1, stepper2, 35)
        move_forward(stepper1, stepper2, 25)
    else:
        turn_left(stepper1, stepper2, 32)
        move_forward(stepper1, stepper2, 35)
        turn_left(stepper1, stepper2, 32)
        move_forward(stepper1, stepper2, 25)
