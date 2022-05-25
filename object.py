import math
import re


class object:
    shape = None
    material = None
    cx = None
    cy = None
    mass = None
    coordinates = None
    id = None

    def __init__(self, parsed_shape):
        _, Name, Form, CX, CY, Mass, Coordinates = parsed_shape
        self.shape = Form
        self.material = re.sub(r'\d+', '', Name)
        self.cx = CX
        self.cy = CY
        self.mass = Mass
        self.coordinates = Coordinates
        self.id = Name

    def __str__(self):
        return "This Object is of shape {shape}, material {material} and has center ({cx},{cy}) dollars!".format(shape=self.shape, material=self.material, cx=self.cx, cy=self.cy)

    def __eq__(self, other_object):
        if self.material != other_object.material:
            # Objects cannot change material.
            # Assumes vision is robust enough to detect material reliably
            return False
        if self.shape != other_object.shape:
            # Objects cannot change shape
            # Again relies on robust detection.
            return False

        # Compare euclidian distance
        d = math.sqrt(math.pow(float(other_object.cx) - float(self.cx), 2) +
                      math.pow(float(other_object.cy) - float(self.cy), 2))

        threshold = 10  # TODO: What is a good value for threshold?
        if d > threshold:
            return False

        return True

        # TODO: Should mass and/or coordinates be compared?
