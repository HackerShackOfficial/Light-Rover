class LightVector(object):

    def __init__(self, steps, angle, pixel_data):
        """
        :param steps: number of steps to move
        :param angle: angle to turn after the movement
        :param pixel_data: a 2d array of pixel data [[r, g, b]...n] where n is the number of pixels in the matrix
        """
        self.steps = steps
        self.angle = angle
        self.pixel_data = pixel_data


rectangle = [LightVector(300, 90, [[0, 255, 0]]),
             LightVector(200, 90, [[255, 255, 0]]),
             LightVector(300, 90, [[255, 0, 255]]),
             LightVector(200, 90, [[0, 0, 255]])]

star = []
