from abc import ABC, abstractmethod
from matplotlib.patches import Rectangle, Wedge
import numpy as np
import matplotlib.pyplot as plt


class Element(ABC):
    def __init__(self):
        self._hide = False
        self._level = 10

    @abstractmethod
    def boundingbox():
        pass

    @abstractmethod
    def get_base_elements(self):
        pass

    @abstractmethod
    def setlevel():
        pass

    @abstractmethod
    def draw():
        pass

    @abstractmethod
    def hide():
        pass

    def hidden(self):
        return self._hide

    def maybedraw(self, ax):
        if not self.hidden():
            self.draw(ax)

    def surface(self):
        return self.boundingbox().surface()


class BaseElement(Element, ABC):
    def get_base_elements(self):
        return [self]

    def hide(self):
        self._hide = True

    def setlevel(self, level):
        self._level = level


class Box:
    def __init__(self, left, bottom, right, top):
        assert(left <= right)
        assert(bottom <= top)
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def surface(self):
        return (self.right - self.left) * (self.top - self.bottom)

    def edit(self, dleft, dbottom, dright, dtop):
        return Box(self.left + dleft, self.bottom + dbottom,
                   self.right + dright, self.top + dtop)

    def gotop(self):
        return Box(self.left, self.top, self.right, self.top)

    def gobottom(self):
        return Box(self.left, self.bottom, self.right, self.bottom)

    def goleft(self):
        return Box(self.left, self.bottom, self.left, self.top)

    def goright(self):
        return Box(self.right, self.bottom, self.right, self.top)

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(
                key=key, value=self.__dict__[key]))

        return self.__class__.__name__ + "(" + ', '.join(sb) + ")"

    def __repr__(self):
        return self.__str__()


class Collection(Element, ABC):
    def __init__(self):
        super().__init__()
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def draw(self, ax):
        base_elements = self.get_base_elements()
        for element in sorted(
                base_elements, key=lambda x: (x._level, x.surface()),
                reverse=True):
            element.maybedraw(ax)

    def get_base_elements(self, ):
        base_elements = []
        for el in self.elements:
            base_elements += el.get_base_elements()
        return base_elements

    def hide(self):
        for el in self.elements:
            el.hide()

    def setlevel(self, level):
        self._level = level
        for el in self.elements:
            el.setlevel(level)

    def boundingbox(self):
        left = np.inf
        bottom = np.inf
        right = -np.inf
        top = -np.inf
        for el in self.elements:
            box = el.boundingbox()
            left = min(left, box.left)
            bottom = min(bottom, box.bottom)
            right = max(right, box.right)
            top = max(top, box.top)
        return Box(left, bottom, right, top)


class Arrow(BaseElement):
    def __init__(self,
                 x,
                 y,
                 dx,
                 dy,
                 head_width=0.2,
                 head_length=0.2,
                 fc="k",
                 ec="k"):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.head_width = head_width
        self.head_length = head_length
        self.fc = fc
        self.ec = ec

    def draw(self, ax):
        ax.arrow(
            self.x,
            self.y,
            self.dx,
            self.dy,
            head_width=self.head_width,
            head_length=self.head_length,
            fc=self.fc,
            ec=self.ec,
            length_includes_head=True)

    def boundingbox(self):
        return Box(
            min(self.x, self.x + self.dx), min(self.y, self.y + self.dy),
            max(self.x, self.x + self.dx), max(self.y, self.y + self.dy))


class HalfCircle(BaseElement):
    def __init__(self, x, y, r, side, color="white"):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r
        self.side = side
        self.color = color

    def draw(self, ax):
        ax.add_patch(
            Wedge(
                (self.x, self.y),
                self.r,
                self.side.theta1,
                self.side.theta2,
                facecolor=self.color,
                edgecolor="black"))

    def boundingbox(self):
        return Box(self.x - (self.r / 2), self.y - (self.r / 2), self.x,
                   self.y)


class Rect(Box, BaseElement):
    def __init__(self,
                 box,
                 color="white",
                 text=None,
                 textcolor="black",
                 hatch=None,
                 lw=1,
                 edgecolor="black"):
        BaseElement.__init__(self)
        Box.__init__(self, box.left, box.bottom, box.right, box.top)
        self.color = color
        self.text = text
        self.textcolor = textcolor
        self.hatch = hatch
        self.lw = lw
        self.edgecolor = edgecolor

    def draw(self, ax):
        r = Rectangle(
            (self.left, self.bottom),
            self.right - self.left,
            self.top - self.bottom,
            facecolor=self.color,
            ec="black",
            hatch=self.hatch,
            lw=self.lw,
            edgecolor=self.edgecolor)
        ax.add_patch(r)
        if self.text:
            x = (self.left + self.right) / 2
            y = (self.bottom + self.top) / 2
            ax.text(
                x=x,
                y=y,
                s=self.text,
                color=self.textcolor,
                horizontalalignment="center",
                verticalalignment="center")

    def boundingbox(self):
        return self


class Text(BaseElement):
    def __init__(self,
                 x,
                 y,
                 s,
                 horizontalalignment="center",
                 verticalalignment="center"):
        super().__init__()
        self.x = x
        self.y = y
        self.s = s
        self.horizontalalignment = horizontalalignment
        self.verticalalignment = verticalalignment

    def draw(self, ax):
        ax.text(
            x=self.x,
            y=self.y,
            s=self.s,
            horizontalalignment=self.horizontalalignment,
            verticalalignment=self.verticalalignment)

    def boundingbox(self):
        return Box(self.x, self.y, self.x, self.y)


class Plan(Collection):
    def draw(self, figsize=1):
        box = self.boundingbox()

        plt.figure(
            figsize=(figsize * (box.right - box.left) * 1.1,
                     figsize * (box.top - box.bottom)))
        ax = plt.gca()
        super().draw(ax)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.xlim(box.left - 0.5, box.right + 0.5)
        plt.xticks(range(int(box.left), int(box.right)))
        plt.yticks(range(int(box.bottom), int(box.top)))
        plt.ylim(box.bottom - 0.5, box.top + 0.5)
        plt.show()
