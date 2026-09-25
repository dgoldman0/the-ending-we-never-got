(let* ((im (car (gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s045-citadel-north-infirmary/ward-master.xcf" "ward-master.xcf"))) (flat (car (gimp-image-merge-visible-layers im CLIP-TO-IMAGE))))
 (file-png-save RUN-NONINTERACTIVE im flat "/tmp/s045-reopened.png" "/tmp/s045-reopened.png" 0 9 0 0 0 0 0)
 (gimp-image-delete im))
(gimp-quit 0)
