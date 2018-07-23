from enum import Enum, auto
from boekfos.core import Box


class Orientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()

    def box(self, a1, b1, a2, b2):
        assert(a1 <= a2)
        assert(b1 <= b2)

        if self == Orientation.VERTICAL:
            left = a1
            bottom = b1
            right = a2
            top = b2
        elif self == Orientation.HORIZONTAL:
            left = b1
            bottom = a1
            right = b2
            top = a2
        else:
            raise Exception(str(self))
        return Box(left, bottom, right, top)

    def line(self, a, b1, b2):
        return self.box(a, b1, a, b2)

    def point(self, a, b):
        return self.box(a, b, a, b)


class Side(Enum):
    BOTTOM = (180, 0, 270, -1)
    LEFT = (90, 270, 180, -1)
    RIGHT = (270, 90, 360, 1)
    TOP = (0, 180, 90, 1)

    def __init__(self, theta1, theta2, degrees, multiplier):
        self.theta1 = theta1
        self.theta2 = theta2
        self.degrees = degrees
        self.multiplier = multiplier

    def orientation(self):
        if self in [Side.LEFT, Side.RIGHT]:
            # The left side is a vertical line
            return Orientation.VERTICAL
        else:
            # the bottom side is a horizontal table
            return Orientation.HORIZONTAL

    def deltapair(self, x, dx):
        if self in [Side.LEFT, Side.BOTTOM]:
            return x - dx, x
        else:
            return x, x + dx

    def delta(self, x, dx):
        if self in [Side.LEFT, Side.BOTTOM]:
            return x - dx
        else:
            return x + dx

    def a(self, box):
        if self == Side.LEFT:
            return box.left
        if self == Side.RIGHT:
            return box.right
        if self == Side.TOP:
            return box.top
        if self == Side.BOTTOM:
            return box.bottom

    def b1(self, box):
        if self in [Side.LEFT, Side.RIGHT]:
            # The left side is a vertical line
            return box.bottom
        else:
            # the bottom side is a horizontal line
            return box.left

    def a1(self, box):
        if self in [Side.LEFT, Side.RIGHT]:
            # The left side is a vertical line
            return box.left
        else:
            # the bottom side is a horizontal line
            return box.bottom

    def a2(self, box):
        if self in [Side.LEFT, Side.RIGHT]:
            # The left side is a vertical line
            return box.right
        else:
            # the bottom side is a horizontal line
            return box.top

    def b2(self, box):
        if self in [Side.LEFT, Side.RIGHT]:
            # The left side is a vertical line
            return box.top
        else:
            # the bottom side is a horizontal line
            return box.right
