from boekfos.core import Rect


#class Garden(Rect):
#    def __init__(self, box):
#        super().__init__(box, color="lightgreen")


class Terrace(Rect):
    def __init__(self, box):
        super().__init__(box, color="lightgrey")


class Carpark(Rect):
    def __init__(self, box):
        super().__init__(box, color="#f5f5dc")


class Roof(Rect):
    def __init__(self, box):
        super().__init__(box, color="#9f8170")
