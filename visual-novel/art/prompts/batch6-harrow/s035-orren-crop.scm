(let* ((im(car(gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/batch6-harrow/s035-collapse/before.png" "visual-novel/art/scene-studies/batch6-harrow/s035-collapse/before.png")))(l 0))
(gimp-image-crop im 385 220 990 130)(set! l(car(gimp-image-get-active-layer im)))
(file-png-save RUN-NONINTERACTIVE im l "visual-novel/art/scene-studies/batch6-harrow/s035-collapse/orren-leg-target.png" "visual-novel/art/scene-studies/batch6-harrow/s035-collapse/orren-leg-target.png" 0 9 0 0 0 0 0)
(gimp-image-delete im))(gimp-quit 0)