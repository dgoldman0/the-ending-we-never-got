(let* ((im(car(gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/batch6-northern/s038-northern-stores-office/repair-master.xcf" "visual-novel/art/scene-studies/batch6-northern/s038-northern-stores-office/repair-master.xcf"))) (f 0))
(set! f(car(gimp-image-merge-visible-layers im CLIP-TO-IMAGE)))
(file-png-save RUN-NONINTERACTIVE im f "/tmp/s038-reopened.png" "/tmp/s038-reopened.png" 0 9 0 0 0 0 0)
(gimp-image-delete im))(gimp-quit 0)