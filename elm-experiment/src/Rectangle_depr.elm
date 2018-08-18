module Rectangle exposing ( initLBRT
  , initXYWH
  , x
  , y
  , width
  , height
  , left
  , right
  , bottom
  , top
  , get
  , set
  , update
  , view
  , Model)

import Html
import Svg as S
import Svg.Attributes as A

-- MODEL

type alias Rectangle =
    { x : Float
    , y : Float
    , width : Float
    , height : Float
    }

initXYWH = Rectangle

initLBRT l b r t =
  { x = l
  , y = b
  , width = r - l
  , height = t - b
  }

type alias Lens a b
 = (b -> a, b -> a -> b)

x : Lens Float Model
x = (.x , setX)
setX model x = {model | x = x }

y : Lens Float Model
y = (.y , setY)
setY model y = {model | y = y }

width : Lens Float Model
width = (.width , setWidth)
setWidth model width = {model | width = width }

height : Lens Float Model
height = (.height , setY)
setHeight model height = {model | height = height }

left : Lens Float Model
left = (.x , setLeft)
setLeft model left = {model | y = left }

right : Lens Float Model
right = ((\model -> model.x + model.width) , setRight)
setRight : Model -> Float -> Model
setRight model right =
  { model | width = right - get left model}

bottom : Lens Float Model
bottom = (.y , setTop)
setBottom model bottom = {model | y = bottom }

top : Lens Float Model
top = ((\model -> model.y - model.width) , setBottom)
setTop model top =
  { model | height = top - get bottom model}

get (getter, setter) = getter

set (getter, setter) = setter

update lens model f
  = set lens model (f (get lens model))


view : Model -> Html.Html ()
view model =
  S.rect
    [ A.x (toString (get x model))
    , A.y (toString (get y model))
    , A.width (toString (get width model))
    , A.height (toString (get height model))
    ]
    []
