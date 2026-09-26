(let* ((im(car(gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s057-father/framed-master.xcf" "visual-novel/art/scene-studies/s057-father/framed-master.xcf")))(f 0))
(set! f(car(gimp-image-merge-visible-layers im CLIP-TO-IMAGE)))
(file-png-save RUN-NONINTERACTIVE im f "/tmp/batch6-s057-father-reopen.png" "/tmp/batch6-s057-father-reopen.png" 0 9 0 0 0 0 0)
(gimp-image-delete im))(gimp-quit 0)
