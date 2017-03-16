# Light-Rover
Light painting robot

This section is a WIP. More detailed instructions coming soon.

## Installing Dependencies

Make sure you install the following dependencies:
```
Pillow
RPi.GPIO
numpy
```

We also used a custom Raspberry Pi Neopixel library found here: https://github.com/jgarff/rpi_ws281x

Follow the Raspberry Pi install instructions.

At the bottom of light_rover.py, we configure the pins for all of our components.
Make sure these pins are correct.

```python
stepper1 = Stepper(2, 3, 4, 17)
stepper2 = Stepper(27, 22, 10, 9)
```

```python
led_matrix = create_strip(64, led_pin=18)
```

## Drawing Vectors

Make sure the following section is commented out at the end of `light_rover.py`

```python
if imageFile:
        rover.paint_image(imageFile)
    else:
        print "No image file provided!"
        exit(1)
```

Uncomment the following line

```python
rover.paint_vector(dog, single_value_affects_pixels=[27, 28, 35, 36])
```

Choose a vector from the `vector_drawings.py` file and change that value
in the `paint_vector` function.

To run, make sure you are in the project directory and execute:

```shell
sudo python light_rover.py
```

## Drawing Images

Make sure the following section is commented out at the end of `light_rover.py`

```python
rover.paint_vector(dog, single_value_affects_pixels=[27, 28, 35, 36])
```

Uncomment the following line

```python
if imageFile:
        rover.paint_image(imageFile)
    else:
        print "No image file provided!"
        exit(1)
```

To run, make sure you are in the project directory and execute:

```shell
sudo python light_rover.py images/sb.png
```