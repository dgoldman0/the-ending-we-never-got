(let* ((img(car(gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/s043-upper-stores/upper-stores-master.xcf" "visual-novel/art/scene-studies/s043-upper-stores/upper-stores-master.xcf"))))
(gimp-message(string-append "S043 layer count: " (number->string(car(gimp-image-get-layers img)))))
(let* ((ly(car(gimp-image-merge-visible-layers img CLIP-TO-IMAGE))))(file-png-save RUN-NONINTERACTIVE img ly "/tmp/s043-upper-stores-reopened.png" "/tmp/s043-upper-stores-reopened.png" 0 9 0 0 0 0 0))
(gimp-image-delete img))(gimp-quit 0)
