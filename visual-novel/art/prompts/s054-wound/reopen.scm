(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s054-wound/wound-delivery-master.xcf" "master"))) (flat (car (gimp-image-merge-visible-layers img CLIP-TO-IMAGE))))
 (file-png-save RUN-NONINTERACTIVE img flat "/tmp/s054-wound-reopened.png" "check" 0 9 0 0 0 0 0)
 (gimp-image-delete img))
(gimp-quit 0)
