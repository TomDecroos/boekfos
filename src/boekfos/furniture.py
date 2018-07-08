from boekfos.core import Rect, HalfCircle, Collection, Box, Arrow, BaseElement
from matplotlib.patches import Wedge
import numpy as np


class Closet(Rect):
    def __init__(self, box):
        super().__init__(box, color="lightgrey")


class Furniture(Rect):
    def __init__(self, box):
        super().__init__(box, color="white")


class Table(Furniture):
    def chair(self, side, i, n):
        b1 = side.b1(self)
        b2 = side.b2(self)
        b = b1 + ((b2 - b1) / (n + 1) * (i + 1))
        a = side.a(self)
        point = side.orientation().point(a, b)
        return Chair(point.left, point.bottom, side)


class Chair(HalfCircle):
    def __init__(self, x, y, side):
        super().__init__(x, y, 0.25, side, color="white")


class Sink(HalfCircle):
    def __init__(self, x, y, side):
        super().__init__(x, y, 0.25, side, color="white")


class Shower(Rect):
    def __init__(self, box):
        super().__init__(box, color="white")


class Toilet(Collection):
    def __init__(self, x, y, side):
        super().__init__()
        point = Box(x, y, x, y)
        a = side.a(point)
        a1, a2 = side.deltapair(a, 0.3)
        b1, b2 = side.b1(point) - 0.4, side.b2(point) + 0.4
        toiletbox = Furniture(side.orientation().box(a1, b1, a2, b2))
        self.add(toiletbox)
        a = side.a(toiletbox)
        b = (side.b1(toiletbox) + side.b2(toiletbox)) / 2
        chairpoint = side.orientation().point(a, b)
        toiletchair = Chair(chairpoint.left, chairpoint.bottom, side)
        self.add(toiletchair)


class Stairs(Collection):
    def __init__(self, side, box, n):
        super().__init__()
        b1 = side.b1(box)
        b2 = side.b2(box)
        a1 = side.a1(box)
        a2 = side.a2(box)

        ais = np.linspace(a1, a2, n)
        for ai, aj in zip(ais[:-1], ais[1:]):
            boxi = side.orientation().box(ai, b1, aj, b2)
            self.add(Furniture(boxi))
        #arrowstart = side.box(side.a
        #self.add(Arrow(


class Door(BaseElement):
    def __init__(self, x, y, degrees2, degrees1, doorwidth=0.85):
        super().__init__()
        self.x = x
        self.y = y
        self.degrees2 = degrees2
        self.degrees1 = degrees1
        self.doorwidth = doorwidth

    def boundingbox(self):
        return Box(0, 0, 1, 1)

    def draw(self, ax):
        a, b, c = self.degrees2 - 360, self.degrees2, self.degrees2 + 360
        d2 = min([a, b, c], key=lambda x: abs(x - self.degrees1))
        d1 = self.degrees1
        if d1 > d2:
            d1, d2 = d2, d1
        ax.add_patch(
            Wedge(
                (self.x, self.y), self.doorwidth, d1, d2, fill=False, ls=":"))
