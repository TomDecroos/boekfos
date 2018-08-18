import Html
import Svg as S
import Svg.Attributes as A
import DrawableCollection exposing (garden, terrace)

import List exposing (minimum, maximum)
import Maybe exposing (withDefault)
import Box
import String

main =
  Html.program
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    }

-- MODEL

type alias Model = DrawableCollection.Model

init : (Model, Cmd ())
init =
  ( DrawableCollection.DrawableCollection [
    terrace -1 -1 9 18
    , garden -4 -6 12 36
    ]
  , Cmd.none
  )

-- UPDATE

update msg model = (model, Cmd.none )


-- SUBSCRIPTIONS

subscriptions : Model -> Sub ()
subscriptions model = Sub.none

-- VIEW

type Msg
  = Nothing ()

view = DrawableCollection.view
