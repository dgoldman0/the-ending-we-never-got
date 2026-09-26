(let* ((im(car(gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/batch6-continuity/s042-cart/before.png" "visual-novel/art/scene-studies/batch6-continuity/s042-cart/before.png")))(l 0))
(gimp-image-crop im 410 510 980 280)(set! l(car(gimp-image-get-active-layer im)))
(file-png-save RUN-NONINTERACTIVE im l "visual-novel/art/scene-studies/batch6-continuity/s042-cart/cart-target.png" "visual-novel/art/scene-studies/batch6-continuity/s042-cart/cart-target.png" 0 9 0 0 0 0 0)
(gimp-image-delete im))(gimp-quit 0)