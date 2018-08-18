module Shape exposing (..)

import Box
import Svg
import Svg.Attributes as A
import Html

type Model
  = Rectangle Left Bottom Right Top
  | HalfCircle X Y Radius Dir

type alias Left = Float
type alias Bottom = Float
type alias Right = Float
type alias Top = Float

type alias X = Float
type alias Y = Float
type alias Radius = Float

type Dir
  = Left
  | Top
  | Bottom
  | Right


initRectangle l b r t =
  Rectangle l b r t


bbox : Model -> Box.Model
bbox shape =
  case shape of
    Rectangle l b r t ->
      Box.Model l b r t
    HalfCircle x y r dir->
      Box.Model (x-r) (y-r) (x+r) (y+r)

-- view

view : Model -> Html.Html ()
view model
  = (tag model) (attributes model) []

tag model =
  case model of
    Rectangle l b r t ->
      Svg.rect
    HalfCircle _ _ _ _ ->
      Svg.circle

attributes model =
  case model of
    Rectangle l b r t ->
      [ A.x (toString l)
      , A.y (toString b)
      , A.width (toString (r - l))
      , A.height (toString (t - b))
      ]
    HalfCircle _ _ _ _ ->
      []
