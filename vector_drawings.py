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


class LightPixel(object):

    def __init__(self, r, g, b, pos):
        self.r = r
        self.g = g
        self.b = b
        self.pos = pos


rectangle = [LightVector(1000, 90, [[0, 255, 0]]),
             LightVector(800, 90, [[0, 255, 255]]),
             LightVector(1000, 90, [[0, 255, 0]]),
             LightVector(800, 90, [[0, 255, 255]])]

star = [LightVector(600, -72, [[0, 255, 0]]),
        LightVector(600, 144, [[255, 255, 0]]),
        LightVector(600, -72, [[255, 0, 255]]),
        LightVector(600, 144, [[0, 0, 255]]),
        LightVector(600, -72, [[0, 0, 255]]),
        LightVector(600, 144, [[0, 255, 0]]),
        LightVector(600, -72, [[255, 255, 0]]),
        LightVector(600, 144, [[255, 0, 255]]),
        LightVector(600, -72, [[0, 0, 255]]),
        LightVector(600, 144, [[0, 0, 255]])]

rectangle_pos = [LightVector(1000, 90, [LightPixel(0, 255, 0, 27), LightPixel(0, 255, 0, 28), LightPixel(0, 255, 0, 35), LightPixel(0, 255, 255, 36)]),
             LightVector(800, 90, [LightPixel(0, 255, 0, 27), LightPixel(0, 255, 0, 28), LightPixel(0, 255, 0, 35), LightPixel(255, 255, 0, 36)]),
             LightVector(1000, 90, [LightPixel(0, 255, 0, 27), LightPixel(0, 255, 0, 28), LightPixel(0, 255, 0, 35), LightPixel(0, 255, 255, 36)]),
             LightVector(800, 90, [LightPixel(0, 255, 0, 27), LightPixel(0, 255, 0, 28), LightPixel(0, 255, 0, 35), LightPixel(255, 255, 0, 36)])]

tree = [LightVector(350, -90, [[210, 105, 30]]),
            LightVector(380, 133, [[0, 255, 0]]),
            LightVector(500, -133, [[0, 255, 0]]),
            LightVector(250, 133, [[0, 255, 0]]),
            LightVector(400, -133, [[0, 255, 0]]),
            LightVector(140, 133, [[0, 255, 0]]),
            LightVector(400, 86, [[0, 255, 0]]),
            LightVector(400, 133, [[0, 255, 0]]),
            LightVector(140, -133, [[0, 255, 0]]),
            LightVector(400, 133, [[0, 255, 0]]),
            LightVector(250, -133, [[0, 255, 0]]),
            LightVector(500, 133, [[0, 255, 0]]),
            LightVector(380, -90, [[0, 255, 0]]),
            LightVector(350, 90, [[210, 105, 30]]),
            LightVector(233, 90, [[210, 105, 30]])]

dog = [LightVector(75, 11, [[210, 105, 30]]),
        LightVector(75, 55, [[210, 105, 30]]),
        LightVector(115, 35, [[210, 105, 30]]),
        LightVector(243, -21, [[210, 105, 30]]),
        LightVector(60, -141, [[210, 105, 30]]),
        LightVector(203, 51, [[210, 105, 30]]),
        LightVector(115, 111, [[210, 105, 30]]),
        LightVector(100, 26, [[210, 105, 30]]),
        LightVector(292, 18, [[210, 105, 30]]),
        LightVector(150, 25, [[210, 105, 30]]),
        LightVector(204, 10, [[210, 105, 30]]),
        LightVector(327, 11, [[210, 105, 30]]),
        LightVector(288, -101, [[210, 105, 30]]),
        LightVector(79, 145, [[210, 105, 30]]),
        LightVector(123, -94, [[210, 105, 30]]),
        LightVector(103, 129, [[210, 105, 30]]),
        LightVector(99, -41, [[210, 105, 30]]),
        LightVector(103, 7, [[210, 105, 30]]),
        LightVector(160, 90, [[210, 105, 30]]),
        LightVector(87, 56, [[210, 105, 30]]),
        LightVector(130, -38, [[210, 105, 30]]),
        LightVector(87, 31, [[210, 105, 30]]),
        LightVector(126, -40, [[210, 105, 30]]),
        LightVector(146, -82, [[210, 105, 30]]),
        LightVector(167, -26, [[210, 105, 30]]),
        LightVector(99, -33, [[210, 105, 30]]),
        LightVector(38, 54, [[210, 105, 30]]),
        LightVector(67, 122, [[210, 105, 30]]),
        LightVector(158, 48, [[210, 105, 30]]),
        LightVector(351, -52, [[210, 105, 30]]),
        LightVector(246, -34, [[210, 105, 30]]),
        LightVector(225, -47, [[210, 105, 30]]),
        LightVector(143, -77, [[210, 105, 30]]),
        LightVector(102, 42.6, [[210, 105, 30]]),
        LightVector(57, 109.4, [[210, 105, 30]])]
