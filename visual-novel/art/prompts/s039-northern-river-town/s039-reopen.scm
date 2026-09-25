(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s039-northern-river-town/local-finish-master.xcf" "visual-novel/art/scene-studies/s039-northern-river-town/local-finish-master.xcf"))) (flat (car (gimp-image-merge-visible-layers img CLIP-TO-IMAGE))))
(file-png-save RUN-NONINTERACTIVE img flat "/tmp/s039-reopen.png" "/tmp/s039-reopen.png" 0 9 0 0 0 0 0)
(gimp-image-delete img))
(gimp-quit 0)
