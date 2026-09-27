(load "visual-novel/art/prompts/batch7-citadel/compose.scm")
(define (keep img mask points)
(gimp-image-select-polygon img CHANNEL-OP-REPLACE (vector-length points) points)
(gimp-selection-grow img 1)
(gimp-selection-feather img 0.6)
(gimp-context-set-foreground '(0 0 0))
(gimp-edit-fill mask FOREGROUND-FILL)
(gimp-selection-none img))
(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE "visual-novel/art/scene-studies/batch7-citadel/s054-rejected-rear-head.xcf" "current source with portrait-matched Valcair head"))) (layer 0) (mask 0))
(set! layer (patch img "visual-novel/art/scene-studies/batch7-citadel/s054-dais-donor.png" "Three equal limestone risers and plain dais; original actors/objects excluded" 1920 1081 0 0 #(0 658 397 483 672 419 1010 446 1280 502 1604 603 1710 678 1755 716 1770 1080 0 1080) 2))
(set! mask (car (gimp-layer-get-mask layer)))
; Existing Tessa, including both hands, legs and boots.
(keep img mask #(781 390 855 389 916 410 971 441 992 477 1004 512 1004 554 1013 567 1035 577 1052 621 1047 645 1058 659 1072 700 1083 733 1091 742 1097 753 1106 774 1120 791 1120 808 1108 817 1089 820 1069 811 1044 800 1025 782 1020 766 1016 751 1007 742 998 718 984 686 958 659 941 628 931 614 926 609 910 578 866 582 844 641 832 685 828 705 822 727 807 773 790 807 799 830 798 844 778 850 760 843 753 836 750 823 751 802 760 777 758 754 755 716 748 695 746 669 741 650 722 623 699 602 704 579 713 552 724 523 736 494 756 451))
; Throne, lever and pedestal remain their original construction.
(keep img mask #(389 0 655 0 655 457 729 433 750 450 755 737 697 770 653 793 653 832 634 843 596 835 393 714))
(keep img mask #(775 737 860 699 1019 705 1025 728 1024 907 910 982 776 914))
(keep img mask #(830 731 830 706 843 686 878 675 914 631 941 591 914 605 900 609 903 585 933 572 985 551 1012 557 1027 573 1017 587 990 597 966 598 942 633 903 679 873 722 873 740))
; Fallen Valcair and the complete rigid spear.
(keep img mask #(962 300 1344 300 1370 490 1355 518 1329 533 1282 530 1257 520 1247 495 1181 482 1114 473 1045 467 995 453 978 444))
(keep img mask #(1250 500 1415 552 1459 565 1480 583 1537 635 1484 614 1444 595 1397 575 1253 517))
; Tessa's set-aside sword.
(keep img mask #(1066 585 1086 584 1147 619 1148 632 1324 771 1322 779 1130 639 1109 644 1104 635 1112 627 1070 610))
(finish img "visual-novel/art/scene-studies/batch7-citadel/s054-rejected-rear-flush"))
(gimp-quit 0)
