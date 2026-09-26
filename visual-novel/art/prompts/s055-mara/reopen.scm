(let* ((im (car (gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s055-mara/mara-master.xcf" "mara-master.xcf"))) (flat (car (gimp-image-merge-visible-layers im CLIP-TO-IMAGE))))
(file-png-save RUN-NONINTERACTIVE im flat "/tmp/s055-mara-reopened.png" "/tmp/s055-mara-reopened.png" 0 9 0 0 0 0 0)
(gimp-image-delete im)) (gimp-quit 0)
