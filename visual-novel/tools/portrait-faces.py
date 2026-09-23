#!/usr/bin/env python3
"""Measure the face in every dialogue portrait so frames share one head scale.

The reading screens scale each portrait by its face box and centre the frame
on it (ui-reading.rpy, portrait_cameo). Run this after adding portraits:

    python3 visual-novel/tools/portrait-faces.py

Faces come from OpenCV's frontal-face detector on the portrait composited over
grey. Portraits it cannot read are listed; give them a manual box under
"overrides" in renpy/game/portrait-faces.json ([x, y, size] in image pixels).
"""
from pathlib import Path
import json

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'renpy/game'
DATA = GAME / 'portrait-faces.json'
FOLDERS = ['art/cast', 'art/portraits']
NOTE = ('Face boxes [x, y, size] in each dialogue portrait, measured by tools/portrait-faces.py '
        '(OpenCV). "overrides" holds manual boxes for portraits the detector cannot read; they take '
        'precedence. Portrait frames scale by the box and centre on it.')


def detect(path, detector):
    image = Image.open(path).convert('RGBA')
    ground = Image.new('RGBA', image.size, (128, 128, 128, 255))
    ground.alpha_composite(image)
    grey = cv2.equalizeHist(cv2.cvtColor(np.array(ground.convert('RGB')), cv2.COLOR_RGB2GRAY))
    minimum = max(40, min(image.size) // 4)
    faces = detector.detectMultiScale(grey, 1.05, 4, minSize=(minimum, minimum))
    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda box: box[2])
    return [int(x), int(y), int(w)]


def main():
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    previous = json.loads(DATA.read_text()) if DATA.exists() else {}
    overrides = previous.get('overrides', {})
    faces, missing = {}, []
    for folder in FOLDERS:
        for path in sorted((GAME / folder).glob('*.png')):
            if path.stem in overrides:
                continue
            box = detect(path, detector)
            if box:
                faces[path.stem] = box
            else:
                missing.append(path.relative_to(GAME).as_posix())
    DATA.write_text(json.dumps({'_note': NOTE, 'faces': faces, 'overrides': overrides}, indent=1) + '\n')
    print(f'{len(faces)} portraits measured, {len(overrides)} manual overrides.')
    if missing:
        print('No face found; add an override for:')
        for path in missing:
            print('  ' + path)


if __name__ == '__main__':
    main()
