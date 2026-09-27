(load "visual-novel/art/prompts/batch7-citadel/compose.scm")
(let* ((src "visual-novel/art/scene-studies/s054-duel/batch7/13-empty-hall.png") (img (car (gimp-file-load RUN-NONINTERACTIVE src src))) (base (car (gimp-image-get-active-layer img))))
(gimp-item-set-name base "Original empty hall — three-riser dais and impact edge unchanged")
; Reconstruct the slim floor strips exposed beside the old, wider base.
; Source floor pixels come from the adjacent original hall at the same y, without scale.
(patch img src "Remove old left pedestal edge with adjacent same-depth floor" 1672 941 32 0 #(491 541 529 541 531 646 493 653) 5)
(patch img src "Remove old right pedestal edge with adjacent same-depth floor" 1672 941 -37 0 #(610 541 641 541 642 654 609 654) 5)
; Continue actual column shaft texture by 140px, matching its unchanged x525..615 faces.
(patch img src "Extend original cylindrical shaft downward without horizontal distortion" 1672 941 0 140 #(522 521 616 521 616 690 522 690) 4)
; Original mouldings and foot translated downward140px, placing floor contact near y780.
(patch img src "Original column moulding and foot translated +140y" 1672 941 0 140 #(530 670 596 670 607 675 611 681 615 684 616 690 622 695 624 704 626 710 627 720 627 776 624 782 506 784 500 779 500 717 504 710 506 704 510 698 513 695 515 686 520 681 526 677) 1)
(finish img "visual-novel/art/scene-studies/s054-duel/batch7/13-empty-hall-near-pillar"))
(gimp-quit 0)
