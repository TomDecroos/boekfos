from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle,Wedge,Polygon
import numpy as np
import scipy.ndimage
import math
import copy
class Collection(object):

    def __init__(self):
        self.items = []
    def add(self,item):
        self.items.append(item)

    def draw(self,ax):
        for item in self.items:
            item.draw(ax)

class FloorPlan(Collection):

    def text(self,x,y,text):
        self.ax.text(x=x,y=y,s=text,
            horizontalalignment="center",
            verticalalignment="center")

    def beton(self,x1,y1,x2,y2):
        self._rectangle(x1,y1,x2,y2,self.betonc)

    def draw(self,figsize=1):
        x1 = np.inf
        y1 =np.inf
        x2 = -np.inf
        y2 = -np.inf
        for item in self.items:
            if isinstance(item,Rect):
                x1 = min(x1,item.x1)
                x2 = max(x2,item.x2)
                y1 = min(y1,item.y1)
                y2 = max(y2,item.y2)

        plt.figure(figsize=(figsize*(x2-x1)*1.1,
            figsize*(y2-y1)))
        ax = plt.gca()
        super().draw(ax)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.xlim(x1-0.5,x2+0.5)
        plt.xticks(range(x1,x2))
        plt.yticks(range(y1,y2))
        plt.ylim(y1-0.5,y2+0.5)
        plt.show()

class Arrow():

    def __init__(self,x,y,dx,dy,
        head_width=0.2,head_length=0.2,fc="k",ec="k"):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.head_width=head_width
        self.head_length=head_length
        self.fc=fc
        self.ec=ec

    def draw(self,ax):
        ax.arrow(self.x,self.y,self.dx,self.dy,
            head_width=self.head_width,
            head_length=self.head_length,
            fc=self.fc,ec=self.ec,
            length_includes_head=True)

class HalfCircle:

    def __init__(self,x,y,r,orientation,color="white"):
        self.x = x
        self.y = y
        self.r = r
        self.orientation = orientation
        self.color = color

    def draw(self,ax):
        if self.orientation == "top":
            theta1 = 0
            theta2 = 180
        elif self.orientation == "left":
            theta1 = 90
            theta2 = 270
        elif self.orientation == "right":
            theta1 = 270
            theta2 = 90
        elif self.orientation == "bottom":
            theta1 = 180
            theta2 = 0
        ax.add_patch(Wedge((self.x,self.y),
                self.r,theta1,theta2,
                facecolor=self.color,edgecolor="black"))


class Rect(object):

    def __init__(self,x1,y1,x2,y2,color="white",
        text=None,textcolor="black",
        hatch=None,
        lw=1,
        edgecolor="black"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.text = text
        self.textcolor = textcolor
        self.hatch = hatch
        self.lw = lw
        self.edgecolor = edgecolor

    def draw(self,ax):
        r = Rectangle((self.x1,self.y1),
            self.x2-self.x1,self.y2-self.y1,
            facecolor=self.color,ec="black",
            hatch=self.hatch,lw=self.lw,
            edgecolor=self.edgecolor)
        ax.add_patch(r)
        if self.text:
            x = (self.x1 + self.x2)/2
            y = (self.y1 + self.y2)/2
            ax.text(x=x,y=y,s=self.text,
                color=self.textcolor,
                horizontalalignment="center",
                verticalalignment="center")

class ComplexRect(object):

    def __init__(self,a,b1,b2,
        orientation,width,color,
        alignment="center"):
        self.a = a
        self.b1 = b1
        self.b2 = b2
        self.orientation=orientation
        self.width = width
        self.alignment = alignment
        self.color = color

    def get_a1a2(self):
        if self.alignment == "left" or self.alignment == "bottom":
            a1=self.a
            a2=self.a+self.width
        elif self.alignment == "center":
            a1 = self.a - (self.width/2)
            a2 = self.a + (self.width/2)
        elif self.alignment == "right" or self.alignment == "top":
            a1 = self.a-self.width
            a2 = self.a
        return a1,a2

    def middle_a(self):
        a1,a2 = self.get_a1a2()
        return (a1+a2)/2

    def draw(self,ax):
        a1,a2 = self.get_a1a2()
        if self.orientation == "v":
            Rect(a1,self.b1,a2,self.b2,self.color).draw(ax)
        elif self.orientation == "h":
            Rect(self.b1,a1,self.b2,a2,self.color).draw(ax)


class Wall(Collection):

    def __init__(self,a,b1,b2,
        orientation,alignment):
        super().__init__()
        r = ComplexRect(a,b1,b2,
            orientation,self.width,self.color,
            alignment)
        self.add(r)

    @classmethod
    def horizontal(cls,y,x1,x2,alignment="center"):
        return cls(y,x1,x2,"h",alignment)

    @classmethod
    def vertical(cls,x,y1,y2,alignment="center"):
        return cls(x,y1,y2,"v",alignment)

    def window(self,b1,b2):
        for item in self.items:
            if item.b1 < b1 and item.b2 > b2:
                itcopy = copy.copy(item)
                itcopy.b1 = b2
                item.b2 = b1
                window = ComplexRect(item.middle_a(),
                    b1,b2,item.orientation,
                    Window.width,Window.color,"center")
        
        self.add(itcopy)
        self.add(window)

    def door(self,b,alignment1,alignment2,doorwidth=0.85):
        otherb = b + get_multiplier(alignment1)*doorwidth

        if otherb < b:
            b1,b2 = otherb,b
        else:
            b1,b2 = b,otherb

        for item in self.items:
            if isinstance(item,ComplexRect) and item.b1 < b1 and item.b2 > b2:
                itcopy = copy.copy(item)
                itcopy.b1 = b2
                item.b2 = b1

                a = item.middle_a()
                degrees2 = get_degrees(alignment2)
                degrees1 = get_degrees(alignment1)
                if item.orientation == "v":
                    x,y = a,b
                elif item.orientation == "h":
                    x,y = b,a

                door = Door(x,y,degrees2,
                        degrees1,doorwidth)
        
        self.add(itcopy)
        self.add(door)

class InnerWall(Wall):
    color = "darkgrey"
    width = 0.10

class OuterWall(Wall):
    color="darkgrey"
    width=0.40

class Window:
    color="lightblue"
    width = 0.08


class Door:

    def __init__(self,x,y,degrees2,degrees1,deurwidth = 0.85):
        self.x = x
        self.y = y 
        self.degrees2 = degrees2
        self.degrees1 = degrees1
        self.deurwidth = deurwidth

    def draw(self,ax):
        #sin1 = math.sin(degrees1/180*math.pi)
        #cos1 = math.cos(degrees1/180*math.pi)
        #sin2 = math.sin(degrees2/180*math.pi)
        #cos2 = math.cos(degrees2/180*math.pi)
        #plt.plot([x,x+deurwidth*cos2],[y,y+deurwidth*sin2],c="white",lw=1)
        #plt.plot([x,x+deurwidth*cos2],[y,y+deurwidth*sin2],ls=":",c="k")
        #plt.plot([x,x+deurwidth*cos1],[y,y+deurwidth*sin1],c="k")
        
        a,b,c = self.degrees2-360,self.degrees2,self.degrees2+360
        d2 = min([a,b,c],key=lambda x: abs(x-self.degrees1))
        d1 = self.degrees1
        if d1 > d2:
            d1,d2 = d2,d1
        ax.add_patch(Wedge((self.x,self.y),self.deurwidth,
            d1,d2,fill=False,ls=":"))

def get_degrees(alignment):
    for name,degrees in [("top",90),
                        ("bottom",270),
                        ("left",180),
                        ("right",360)]:
        if alignment == name:
            return degrees
def get_multiplier(alignment):
    for name,m in [("top",1),
                        ("bottom",-1),
                        ("left",-1),
                        ("right",1)]:
        if alignment == name:
            return m
"""
class BaseInnerWall:
    color = "white"
    width = 0.10

class BaseOuterWall:
    color="white"
    width = 0.40

class Window:
    color="lightblue"
    width = 0.08
    def __init__(b1,b2):
        self.b1 = b1
        self.b2 = b2

class Collection:

    def __init__(self,items):
        self.items = items
    def draw(self,ax):
        for item in self.items:
            item.draw(ax)

class Wall:
    @classmethod
    def horizontal(cls,y,x1,x2,alignment,
        windows=[],doors=[]):
        return cls._internal(y,x1,x2,"h",alignment,
            windows,doors)

    @classmethod
    def vertical(cls,x,y1,y2,alignment,
        windows=[],doors=[]):
        return cls._internal(x,y1,y2,"v",alignment,
            windows,doors)

    @classmethod
    def _internal(cls,a,b1,b2,
        orientation,alignment,
        windows,doors):
        items = []
        for b1,b2 in cls._splits(b1,windows,b2):
            w = ComplexRect(a,b1,b2,
                orientation,cls.basecls.width,cls.basecls.color,
                alignment)
            items.append(w)

        for window in windows:
            w = ComplexRect(a,window.b1,window.b2,
                orientation,cls.basecls.width,cls.basecls.color,
                alignment)
            ma = w.middle_a()
            w = ComplexRect(ma,window.b1,window.b2,
                orientation,Window.width,Window.color,
                "center")
            items.append(w)

        return Collection(items)    

    @classmethod
    def _splits(cls,a,tuples,b):
        l = [a] + [x for t in tuples for x in t] + [b]
        for i in range(int(len(l)/2)):
            yield l[2*i],l[2*i+1]

class OuterWall(Wall):
    basecls = BaseOuterWall

class InnerWall(Wall):
    basecls = BaseInnerWall

class Door:

    def __init__(x,y,degrees2,degrees1,deurwidth = 0.85):
        self.x = x
        self.y = y 
        self.degrees2 = degrees2
        self.degrees1 = degrees1
        self.deurwidth = deurwidth

    def draw(ax):
        #sin1 = math.sin(degrees1/180*math.pi)
        #cos1 = math.cos(degrees1/180*math.pi)
        #sin2 = math.sin(degrees2/180*math.pi)
        #cos2 = math.cos(degrees2/180*math.pi)
        #plt.plot([x,x+deurwidth*cos2],[y,y+deurwidth*sin2],c="white",lw=1)
        #plt.plot([x,x+deurwidth*cos2],[y,y+deurwidth*sin2],ls=":",c="k")
        #plt.plot([x,x+deurwidth*cos1],[y,y+deurwidth*sin1],c="k")
        if degrees2 < degrees1:
            degrees1,degrees2 = degrees2,degrees1 
        ax.add_patch(Wedge((x,y),deurwidth,
            degrees1,degrees2,fill=False,ls=":"))
   

"""