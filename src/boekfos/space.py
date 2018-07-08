from boekfos.core import Collection, Rect, Box
from boekfos.orientation import Orientation
from boekfos.wall import Wall, WallType
from abc import ABC
from enum import Enum, auto


class Space(Collection, ABC):
    def __init__(self, walltype, box, spaceconfig, text=None,
                 groundcolor=None):
        super().__init__()

        self.box = spaceconfig.editbox(box, walltype.thickness / 2)

        self.leftwall = Wall(walltype, Orientation.VERTICAL, box.left,
                             box.bottom, box.top)
        self.rightwall = Wall(walltype, Orientation.VERTICAL, box.right,
                              box.bottom, box.top)
        self.topwall = Wall(walltype, Orientation.HORIZONTAL, box.top,
                            box.left, box.right)
        self.bottomwall = Wall(walltype, Orientation.HORIZONTAL, box.bottom,
                               box.left, box.right)
        for w in [
                self.leftwall, self.rightwall, self.topwall, self.bottomwall
        ]:
            self.add(w)

        if text:
            self.add(text)
        if groundcolor:
            r = Rect(box, groundcolor)
            self.add(r)

    @property
    def inner(self):
        return Box(self.leftwall.boundingbox().right,
                   self.bottomwall.boundingbox().top,
                   self.rightwall.boundingbox().left,
                   self.topwall.boundingbox().bottom)

    @property
    def outer(self):
        return Box(self.leftwall.boundingbox().left,
                   self.bottomwall.boundingbox().bottom,
                   self.rightwall.boundingbox().right,
                   self.topwall.boundingbox().top)

    @property
    def center(self):
        return self.box


class SpaceConfig(Enum):
    INNER = auto()
    OUTER = auto()
    CENTER = auto()

    def editbox(self, box, d):
        if self == SpaceConfig.INNER:
            return box.edit(-d, -d, d, d)
        elif self == SpaceConfig.OUTER:
            return box.edit(d, d, -d, -d)
        else:
            return box


class Room(Space):
    def __init__(self, box, spaceconfig=SpaceConfig.CENTER, text=None):
        walltype = WallType.IN
        super().__init__(walltype, box, spaceconfig, text)


class Floor(Space):
    def __init__(self, box, spaceconfig=SpaceConfig.OUTER, text=None):
        walltype = WallType.OUT
        groundcolor = "#e8e8e8"
        d = (walltype.thickness / 2)
        box = box.edit(d, d, -d, -d)
        super().__init__(walltype, box, spaceconfig, text, groundcolor)
