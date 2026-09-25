(let* ((im (car (gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s036-harrow-south-bank/arrival-master.xcf" "visual-novel/art/scene-studies/s036-harrow-south-bank/arrival-master.xcf"))) (flat (car (gimp-image-merge-visible-layers im CLIP-TO-IMAGE))))
 (file-png-save RUN-NONINTERACTIVE im flat "/tmp/s036-arrival-reopened.png" "/tmp/s036-arrival-reopened.png" 0 9 0 0 0 0 0)
 (gimp-image-delete im))
(gimp-quit 0)
