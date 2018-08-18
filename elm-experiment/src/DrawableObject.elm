module DrawableObject exposing (..)

import Shape
import MyColor as Color
import Svg
import Svg.Attributes as A
import Html

-- Model
type alias Model
  = { shape : Shape.Model
    , color : Color.Model
    , hidden : Bool
    }

initRectangle : Color.Model -> Float -> Float -> Float -> Float -> Model
initRectangle color l b r t
  = { shape = Shape.initRectangle l b r t
    , color = color
    , hidden = False
    }

bbox model = Shape.bbox model.shape

garden = initRectangle Color.lightgreen
terrace = initRectangle Color.lightgrey

type Orientation
  = Horizontal
  | Vertical

wall thickness color o a b1 b2
  = case o of
    Horizontal ->
      initRectangle color b1 (a - thickness) b2 (a + thickness)
    Vertical ->
      initRectangle color (a - thickness) b1 (a + thickness) b2

outerwall = wall 0.2 Color.darkgrey
innerwall = wall 0.05 Color.darkgrey



view : Model -> Maybe (Html.Html ())
view model =
  let
    view2 model
      = (Shape.tag model.shape) (attributes model) []
  in
    if not model.hidden then
      Just (view2 model)
    else
      Nothing

attributes : Model -> List (Svg.Attribute msg)
attributes model =
  Shape.attributes model.shape
  ++ [A.fill  model.color]
