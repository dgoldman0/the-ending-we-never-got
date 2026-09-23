; GIMP 2.10 Script-Fu for tools/crop-portraits.py. Each portrait is a
; rectangular crop of its source painting; nothing is cut out. Layers in the
; saved master: the source painting (cropped and scaled, with its outline
; repairs), then the ground and vignette layers, all editable.

(define (radial-fill layer w h inner outer)
  (gimp-context-set-foreground inner)
  (gimp-context-set-background outer)
  (gimp-context-set-gradient-fg-bg-rgb)
  (gimp-drawable-edit-gradient-fill layer GRADIENT-RADIAL 0 FALSE 1 0.0 TRUE
                                    (/ w 2) (* h 0.38) (/ w 2) (* h 1.05)))

(define (select-ground image layer seeds threshold)
  ; Contiguous ground from seeds that Python verified are ground, never hair.
  (gimp-context-set-sample-merged FALSE)
  (gimp-context-set-sample-criterion SELECT-CRITERION-COMPOSITE)
  (gimp-context-set-sample-threshold threshold)
  (gimp-selection-none image)
  (let loop ((s seeds))
    (if (and (pair? s) (pair? (cdr s)))
        (begin
          (gimp-image-select-contiguous-color image CHANNEL-OP-ADD layer (car s) (cadr s))
          (loop (cddr s))))))

(define (cutout-ground image layer w h shrink)
  ; A generator cut-out: pull the matte in and soften its stair steps (the
  ; fringe carries black and red from the hidden ground), then paint a
  ; ground beneath.
  (gimp-image-select-item image CHANNEL-OP-REPLACE layer)
  (if (> shrink 0) (gimp-selection-shrink image shrink))
  (gimp-selection-feather image 2.0)
  (let ((mask (car (gimp-layer-create-mask layer ADD-MASK-SELECTION))))
    (gimp-layer-add-mask layer mask))
  (gimp-selection-none image)
  (let ((ground (car (gimp-layer-new image w h RGB-IMAGE "Painted ground" 100 LAYER-MODE-NORMAL))))
    (gimp-image-insert-layer image ground 0 1)
    (radial-fill ground w h '(46 41 38) '(13 13 16))))

(define (grey-ground image layer w h seeds)
  ; Tessa's heads sit on a grey studio ground: take it down toward the others,
  ; feathered so loose strands keep their edges.
  (if (pair? seeds)
      (begin
        (select-ground image layer seeds 0.07)
        (gimp-selection-feather image 10)
        (gimp-drawable-curves-spline layer HISTOGRAM-VALUE 6 #(0.0 0.0 0.45 0.19 1.0 0.6))
        (gimp-selection-none image))))

(define (vignette image w h)
  (let ((v (car (gimp-layer-new image w h RGB-IMAGE "Vignette (multiply)" 60 LAYER-MODE-MULTIPLY))))
    (gimp-image-insert-layer image v 0 0)
    (gimp-context-set-foreground '(255 255 255))
    (gimp-context-set-background '(96 94 100))
    (gimp-context-set-gradient-fg-bg-rgb)
    (gimp-drawable-edit-gradient-fill v GRADIENT-RADIAL 0 FALSE 1 0.0 TRUE
                                      (/ w 2) (* h 0.42) (/ w 2) (* h 1.1))))

(define (crop-portrait src out-png out-xcf x y w h ow oh ground seeds)
  (let* ((image (car (gimp-file-load RUN-NONINTERACTIVE src src)))
         (source (car (gimp-image-get-active-layer image))))
    (gimp-image-undo-disable image)
    (gimp-item-set-name source "Source painting (cropped, not cut out)")
    (gimp-image-crop image w h x y)
    (gimp-context-set-interpolation INTERPOLATION-NOHALO)
    (gimp-image-scale image ow oh)
    (cond ((equal? ground "cutout") (cutout-ground image source ow oh 1))
          ((equal? ground "bust") (cutout-ground image source ow oh 0))
          ((equal? ground "grey") (grey-ground image source ow oh seeds)))
    (vignette image ow oh)
    (gimp-xcf-save 0 image source out-xcf out-xcf)
    (let* ((copy (car (gimp-image-duplicate image)))
           (flat (car (gimp-image-flatten copy))))
      (file-png-save RUN-NONINTERACTIVE copy flat out-png out-png 0 9 0 0 0 0 0)
      (gimp-image-delete copy))
    (gimp-image-delete image)))
