# Portrait treatment samples (prototype)

Not part of the game. After the user rejected the solid reading panels ("they
block too much of the scene; the old way was better") and found the arch
windows cheap, possibly because of their sharp flat bottom, these samples keep
the old gradient shade and replace the arch with three treatments, each fading
at its base so nothing cuts across the chest:

- `vignette`: no frame; the bust dissolves into the shade.
- `oval`: a portrait miniature with a fine gilt rim.
- `rect`: a plain miniature with a hairline gilt rim.

The listener is smaller and quieter at the far end of the line, the pointer
rule is gone and a lozenge replaces the continue knot. A lacquer-toned version
of the gradient (deep celadon with grain) is sampled beside the old one.

`build-frames.py` draws the art into `ui/` (not committed). `sample.py` copies
`zz-frames-prototype.rpy`, a generated capture test and the art into the game
only for the run, removes them, and writes `frames-samples.png`,
`frames-shade.png` and `frames-detail.png` to `renpy/test-output/review/`.
The "current" column reuses the captures made by `prototypes/panel/sample.py`.

## Second round: three ovals, speaker only

The user preferred the oval, with or without an outline, and suggested a
golden halo instead of a solid line, "a bit of a blend"; and asked to drop the
second portrait, since the person spoken to is in the painting. `sample.py`
now captures `oval-bare` (no outline), `oval` (fine gilt line) and
`oval-halo` (a soft gilt glow around the edge, fading at the base), speaker
only, into `ovals-samples.png` and `ovals-detail.png`. The first halo was too
strong (it read as a glowing sticker) and was softened before showing.
