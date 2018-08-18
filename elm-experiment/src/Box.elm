module Box exposing (..)

import Svg
import Html
import Svg.Attributes as A

type alias Model
  = { left : Float
    , bottom : Float
    , right : Float
    , top: Float
    }

width model = model.right - model.left
height model = model.top - model.bottom

surface model = (width model) * (height model)
