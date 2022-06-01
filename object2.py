class object2:
    shape = None
    material = None
    cx = None
    cy = None
    mass = None
    coordinates = None
    id = None

    def __init__(self, obj):
        self.shape = obj.shape
        self.material = obj.material
        self.cx = obj.cx
        self.cy = obj.cy
        self.mass = obj.mass
        self.coordinates = obj.coordinates
        self.id = obj.id

    def __str__(self):
        return "This Object is of shape {shape}, material {material} and has center ({cx},{cy}) dollars!".format(shape=self.shape, material=self.material, cx=self.cx, cy=self.cy)

    # basically the same as object, but compares size instead of position.
    # TODO: not sure if there is a less repetitive way to achieve this
    def __eq__(self, other_object):
        if self.material != other_object.material:
            # Objects cannot change material.
            # Assumes vision is robust enough to detect material reliably
            return False
        if self.shape != other_object.shape:
            # Objects cannot change shape
            # Again relies on robust detection.
            # TODO: can shape change after impact?
            return False

        threshold = 10  # TODO: again a arbitrary threshold
        if((float(self.mass) - float(other_object.mass)) > threshold):
            return False

        return True
