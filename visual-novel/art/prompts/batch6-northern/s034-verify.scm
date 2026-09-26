(let* ((im(car(gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/batch6-northern/s034-return-cargo-shed/repair-master.xcf" "visual-novel/art/scene-studies/batch6-northern/s034-return-cargo-shed/repair-master.xcf"))) (f 0))
(set! f(car(gimp-image-merge-visible-layers im CLIP-TO-IMAGE)))
(file-png-save RUN-NONINTERACTIVE im f "/tmp/s034-reopened.png" "/tmp/s034-reopened.png" 0 9 0 0 0 0 0)
(gimp-image-delete im))(gimp-quit 0)