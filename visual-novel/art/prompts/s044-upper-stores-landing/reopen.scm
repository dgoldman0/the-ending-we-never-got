; Exact visible export of the inspected delivery master, from repository root.
(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s044-upper-stores-landing/landing-delivery-master.xcf" "master")))
       (flat (car (gimp-image-merge-visible-layers img CLIP-TO-IMAGE))))
 (file-png-save RUN-NONINTERACTIVE img flat "/tmp/s044-reopened.png" "reopen" 0 9 0 0 0 0 0)
 (gimp-image-delete img))
