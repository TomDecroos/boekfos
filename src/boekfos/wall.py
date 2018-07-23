from boekfos.core import Collection, Rect
from boekfos.furniture import Closet, Sink, Shower, Table, Toilet, Stairs, Door
from enum import Enum


class Wall(Collection):
    def __init__(self, walltype, orientation, a, b1, b2):
        super().__init__()
        assert (b1 < b2)
        self.orientation = orientation
        self.a = a
        self.b1 = b1
        self.b2 = b2
        self.add(BaseWall(walltype, orientation, a, b1, b2))

    def add(self, element):
        remove_els = set()
        add_els = set()
        if element.walltype != WallType.HOLE:
            add_els.add(element)
        for wall in self.elements:
            if wall.b1 < element.b1 and wall.b2 > element.b1:
                new_b2 = (element.b1 - wall.walltype.thickness / 2 -
                          element.walltype.thickness / 2)
                if new_b2 > wall.b1:
                    new_wall = BaseWall(wall.walltype, wall.orientation,
                                        wall.a, wall.b1, new_b2)
                    new_wall.setlevel(wall._level)
                    add_els.add(new_wall)
                remove_els.add(wall)
            if wall.b2 > element.b2 and wall.b1 < element.b2:
                new_b1 = (element.b2 + wall.walltype.thickness / 2 +
                          element.walltype.thickness / 2)
                if new_b1 < wall.b2:
                    new_wall = BaseWall(wall.walltype, wall.orientation,
                                        wall.a, new_b1, wall.b2)
                    new_wall.setlevel(wall._level)
                    add_els.add(new_wall)
                remove_els.add(wall)

        for el in remove_els:
            self.elements.remove(el)
        for el in add_els:
            self.elements.append(el)

    def applydb(self, db1, db2):
        if db1 >= 0:
            b1 = self.b1 + db1
        else:
            b1 = self.b2 + db1
        if db2 > 0:
            b2 = self.b1 + db2
        else:
            b2 = self.b2 + db2
        return b1, b2

    def window(self, db1, db2):
        b1, b2 = self.applydb(db1, db2)
        window = BaseWall(WallType.WINDOW, self.orientation, self.a, b1, b2)
        self.add(window)

    def hole(self, db1, db2):
        b1, b2 = self.applydb(db1, db2)
        window = BaseWall(WallType.HOLE, self.orientation, self.a, b1, b2)
        self.add(window)

    def door(self, side1, side2, db, doorwidth=0.85):
        if db > 0:
            b = self.b1 + db
        else:
            b = self.b2 + db
        b1, b2 = side1.deltapair(b, doorwidth)
        hole = BaseWall(WallType.HOLE, self.orientation, self.a, b1, b2)
        self.add(hole)
        a = self.a
        degrees2 = side2.degrees
        degrees1 = side1.degrees
        point = side2.orientation().point(a, b)
        self.elements.append(
            Door(point.left, point.bottom, degrees2, degrees1, doorwidth))

    def closet(self, side, da, db1, db2):
        box = self.boundingbox()
        a = side.a(box)
        b1, b2 = self.applydb(db1, db2)
        a1, a2 = side.deltapair(a, da)
        return Closet(side.orientation().box(a1, b1, a2, b2))

    def stairs(self, side, db1, db2):
        box = self.boundingbox()
        a = side.a(box)
        b1, b2 = self.applydb(db1, db2)
        a1, a2 = side.deltapair(a, 2.5)
        return Stairs(side, side.orientation().box(a1, b1, a2, b2), 12)

    def sink(self, side, db, da=0):
        box = self.boundingbox()
        if db > 0:
            b = side.b1(box) + db
        else:
            b = side.b2(box) + db
        a = side.delta(side.a(box), da)
        point = side.orientation().point(a, b)
        return Sink(point.left, point.bottom, side)

    def shower(self, side1, side2, db):
        box = self.boundingbox()
        if db >= 0:
            b = side2.b1(box) + db
        else:
            b = side2.b2(box) + db

        a1, a2 = side2.deltapair(side2.a(box), 1)
        b1, b2 = side1.deltapair(b, 1)

        return Shower(side2.orientation().box(a1, b1, a2, b2))

    def table(self, side, da, db1, db2):
        box = self.boundingbox()
        a = side.a(box)
        b1, b2 = self.applydb(db1, db2)
        a1, a2 = side.deltapair(a, da)
        return Table(side.orientation().box(a1, b1, a2, b2))

    def bureau(self, side, db1, db2):
        table = self.table(side, 0.8, db1, db2)
        chair = table.chair(side, 0, 1)
        c = Collection()
        c.add(table)
        c.add(chair)
        return c

    def bed(self, side1, side2, db):
        box = self.boundingbox()
        if db >= 0:
            b = side2.b1(box) + db
        else:
            b = side2.b2(box) + db

        a1, a2 = side2.deltapair(side2.a(box), 1)
        b1, b2 = side1.deltapair(b, 0.6)
        head = Table(side2.orientation().box(a1, b1, a2, b2))
        b1, b2 = side1.deltapair(b, 2)
        body = Table(side2.orientation().box(a1, b1, a2, b2))
        c = Collection()
        c.add(head)
        c.add(body)
        return c

    def doublebed(self, side1, side2, db):
        box = self.boundingbox()
        if db >= 0:
            b = side2.b1(box) + db
        else:
            b = side2.b2(box) + db

        c = Collection()
        a1, a2 = side2.deltapair(side2.a(box), 0.6)
        b1, b2 = side1.deltapair(b, 0.9)
        c.add(Table(side2.orientation().box(a1, b1, a2, b2)))
        b3, b4 = side1.deltapair(b2, 0.9)
        c.add(Table(side2.orientation().box(a1, b3, a2, b4)))
        a3, a4 = side2.deltapair(side2.a(box), 2)
        c.add(Table(side2.orientation().box(a3, b1, a4, b4)))

        return c

    def toilet(self, side):
        box = self.boundingbox()
        a = side.a(box)
        b = (side.b1(box) + side.b2(box)) / 2
        startpoint = side.orientation().point(a, b)
        return Toilet(startpoint.left, startpoint.bottom, side)


class BaseWall(Rect):
    def __init__(self, walltype, orientation, a, b1, b2):
        self.walltype = walltype
        self.orientation = orientation
        self.a = a
        self.b1 = b1
        self.b2 = b2

        box = orientation.line(a, b1, b2)
        d = walltype.thickness / 2
        box = box.edit(-d, -d, d, d)
        super().__init__(box, walltype.color)


class WallType(Enum):
    IN = ("darkgrey", 0.10)
    OUT = ("darkgrey", 0.40)
    WINDOW = ("lightblue", 0.08)
    HOLE = ("lightgrey", 0)
    HEDGE = ("green", 0.5)

    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness
