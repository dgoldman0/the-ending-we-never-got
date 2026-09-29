(load "visual-novel/art/prompts/batch8-stair/local-compose.scm")
(let* ((source "visual-novel/art/scene-studies/batch8-stair/source-before/s053-bend.png") (img (car (gimp-file-load RUN-NONINTERACTIVE source source))) (layer 0) (mask 0))
(gimp-item-set-name (car (gimp-image-get-active-layer img)) "Current runtime source; complete cast and local horn fixes")
; Remove the enclosed passage with the existing scene's own unobstructed sky.
(set! layer (layer-from-crop img source "Open upper platform: source sky only" 0 0 530 220 1370 0 445 390))
(set! mask (mask-poly img layer #(1370 0 1815 0 1815 390 1370 390) 0.7))
; Carrier and wounded man retain their exact source silhouettes.
(exclude-poly img mask #(1460 59 1466 39 1480 33 1493 30 1509 36 1527 46 1534 64 1532 80 1547 87 1564 79 1581 76 1593 92 1604 121 1610 119 1609 106 1616 94 1630 90 1644 89 1657 101 1665 117 1662 129 1686 141 1703 171 1719 205 1730 240 1749 294 1765 312 1753 335 1736 337 1727 358 1734 389 1725 415 1694 446 1642 490 1431 500 1399 349 1417 219 1428 165 1437 125 1458 96 1480 80) 0.45)
; A grey-brown carrier rather than Olan's close auburn hair; no other body change.
(set! layer (car (gimp-file-load-layer RUN-NONINTERACTIVE img source)))
(gimp-image-insert-layer img layer 0 0)
(gimp-item-set-name layer "Unnamed carrier: dark charcoal-brown hair, source outline")
(gimp-hue-saturation layer ALL-HUES 0 -34 -65)
(mask-poly img layer #(1463 56 1469 41 1481 33 1497 31 1510 35 1525 44 1533 58 1533 67 1528 75 1516 68 1505 71 1495 77 1480 73 1470 68) 1)
; Desaturate and compress the source paving highlights: identical grain and seams.
(set! layer (car (gimp-file-load-layer RUN-NONINTERACTIVE img source)))
(gimp-image-insert-layer img layer 0 0)
(gimp-item-set-name layer "Dry paving: suppress water glare and orange reflected light locally")
(gimp-hue-saturation layer ALL-HUES 0 -7 -75)
(gimp-levels layer HISTOGRAM-VALUE 0 255 0.85 14 185)
(set! mask (mask-poly img layer #(0 1017 205 866 584 824 950 791 1793 792 1840 873 1920 910 1920 1080 0 1080) 18))
; Northern attackers' boots, coats and contact shadows.
(exclude-poly img mask #(190 850 273 797 345 761 422 761 458 785 542 815 564 853 559 889 597 894 600 918 567 940 536 948 505 947 491 961 471 990 454 1018 444 1045 413 1068 361 1079 333 1078 330 1055 351 1008 348 973 294 976 245 969 220 955 231 928 258 894 205 890) 1)
(exclude-poly img mask #(797 753 876 756 892 791 891 822 879 857 877 880 889 908 892 931 904 954 910 983 927 1000 929 1016 912 1032 880 1043 843 1041 811 1041 778 1034 767 1011 766 972 753 946 749 905 746 872 748 832 771 796) 1)
; Mara's stance and boot contact.
(exclude-poly img mask #(901 775 941 775 936 792 937 813 965 830 969 845 955 860 927 866 896 863 874 849 884 829) 1)
(exclude-poly img mask #(1228 764 1260 779 1266 806 1283 830 1310 841 1314 861 1295 872 1270 871 1245 865 1225 855 1224 826) 1)
; Low broad masonry parapet at the top platform, behind the ascending men.
(set! layer (layer-from-crop img source "Upper platform rear parapet; original local masonry" 765 26 420 132 1370 332 445 58))
(set! mask (mask-poly img layer #(1370 332 1815 332 1815 390 1370 390) 0.7))
(exclude-poly img mask #(1406 322 1428 256 1453 301 1494 312 1544 300 1592 326 1636 303 1695 318 1736 310 1751 333 1740 353 1730 388 1729 448 1404 447) 0.6)
; Battle-broken shield fragments. Each contour removes the donor wall and ground.
(set! layer (layer-from-crop img "visual-novel/renpy/game/art/scenes/s055-mara.png" "Broken shield A: closes the flank beside Mara" 0 530 320 225 1308 713 416 293))
(mask-poly img layer #(1308 721 1352 720 1407 747 1438 782 1480 803 1517 830 1551 856 1569 873 1607 891 1627 913 1684 938 1712 944 1716 965 1677 969 1640 961 1593 947 1563 946 1554 969 1529 978 1500 958 1472 985 1448 974 1433 998 1412 987 1387 990 1363 966 1308 993) 1)
(set! layer (layer-from-crop img "visual-novel/renpy/game/art/scenes/s055-mara.png" "Broken shield B: closes to the right wall" 0 530 320 225 1570 670 384 270))
(mask-poly img layer #(1570 677 1611 676 1661 701 1690 734 1728 753 1763 778 1794 802 1811 818 1846 834 1864 855 1917 878 1943 884 1947 903 1911 906 1876 899 1833 886 1805 885 1797 906 1774 915 1748 896 1721 921 1699 910 1685 933 1666 923 1643 926 1620 905 1570 928) 1)
(export-master img "visual-novel/art/scene-studies/batch8-stair/s053-bend-local"))
(gimp-quit 0)
