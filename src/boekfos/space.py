from boekfos.core import Collection, Rect, Box, Text
from boekfos.orientation import Orientation
from boekfos.wall import Wall, WallType
from abc import ABC
from enum import Enum, auto


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


class Space(Collection, ABC):
    def __init__(self,
                 walltype,
                 box,
                 spaceconfig,
                 text=None,
                 groundcolor=None,
                 groundconfig=SpaceConfig.CENTER):
        super().__init__()

        self.box = spaceconfig.editbox(box, walltype.thickness / 2)

        self.leftwall = Wall(walltype, Orientation.VERTICAL, self.box.left,
                             self.box.bottom, self.box.top)
        self.rightwall = Wall(walltype, Orientation.VERTICAL, self.box.right,
                              self.box.bottom, self.box.top)
        self.topwall = Wall(walltype, Orientation.HORIZONTAL, self.box.top,
                            self.box.left, self.box.right)
        self.bottomwall = Wall(walltype, Orientation.HORIZONTAL,
                               self.box.bottom, self.box.left, self.box.right)
        for w in [
                self.leftwall, self.rightwall, self.topwall, self.bottomwall
        ]:
            self.add(w)

        if text:
            x = (box.left + box.right) / 2
            y = (box.bottom + box.top) / 2
            self.add(Text(x, y, text))
        if groundcolor:
            r = Rect(
                groundconfig.editbox(box, walltype.thickness / 2), groundcolor)
            self.add(r)
            self.ground = r

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


class Room(Space):
    def __init__(self, box, spaceconfig=SpaceConfig.CENTER, text=None):
        walltype = WallType.IN
        super().__init__(walltype, box, spaceconfig, text)


class Floor(Space):
    def __init__(self, box, spaceconfig=SpaceConfig.OUTER, text=None):
        walltype = WallType.OUT
        groundcolor = "#e8e8e8"
        super().__init__(
            walltype,
            box,
            spaceconfig,
            text,
            groundcolor,
            groundconfig=SpaceConfig.OUTER)
        lev = self._level
        self.setlevel(9)
        self.ground.setlevel(lev)


class Garden(Space):
    def __init__(self,
                 box,
                 spaceconfig=SpaceConfig.OUTER,
                 grass=True,
                 text=None):
        groundcolor = "lightgreen" if grass else None
        walltype = WallType.HEDGE
        super().__init__(
            walltype,
            box,
            spaceconfig,
            text,
            groundcolor,
            groundconfig=SpaceConfig.CENTER)
