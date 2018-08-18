module DrawableCollection exposing (..)
import Html
import Svg as S
import Svg.Attributes as A

import DrawableObject
import List exposing (minimum, maximum)
import Maybe exposing (withDefault)
import Box
import String

type Model
  = DrawableObject DrawableObject.Model
  | DrawableCollection (List Model)

bbox model =
  case model of
    DrawableObject object ->
      DrawableObject.bbox object

    DrawableCollection collection ->
      let
        boxes = List.map bbox collection
        left = withDefault 0 <| minimum (List.map .left boxes)
        right = withDefault 1 <| maximum (List.map .right boxes)
        top = withDefault 1 <| maximum (List.map .top boxes)
        bottom = withDefault 0 <| minimum (List.map .bottom boxes)
      in
        Box.Model left bottom right top

garden l b r t = DrawableObject <| DrawableObject.garden l b r t
terrace l b r t = DrawableObject <| DrawableObject.terrace l b r t


view : Model -> Html.Html ()
view model =
    S.svg
      [ A.width "100%"
      , A.height "100%"
      , A.viewBox <| viewboxstring <| bbox model
      , A.transform "scale(1,-1)"
      ]
      (List.filterMap DrawableObject.view <| orderbySize <| baseObjects model
      )


baseObjects : Model -> List DrawableObject.Model
baseObjects model =
  case model of
    DrawableObject object ->
      [object]
    DrawableCollection collection ->
      List.concatMap baseObjects collection


orderbySize : List DrawableObject.Model -> List DrawableObject.Model
orderbySize model =
  let surface object = (Box.surface (DrawableObject.bbox object))
  in
    List.reverse <| List.sortBy surface model


viewboxstring box =
  let coords = [box.left, box.bottom, box.right, box.top]
  in
   String.join " " <| List.map toString coords
