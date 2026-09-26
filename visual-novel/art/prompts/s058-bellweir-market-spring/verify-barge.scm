(let* ((im (car (gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s058-bellweir-market-spring/barge-local-master.xcf" "barge master"))) (flat (car (gimp-image-merge-visible-layers im CLIP-TO-IMAGE))))
(file-png-save RUN-NONINTERACTIVE im flat "/tmp/s058-barge-reopened.png" "/tmp/s058-barge-reopened.png" 0 9 0 0 0 0 0)
(gimp-image-delete im))
(gimp-quit 0)
