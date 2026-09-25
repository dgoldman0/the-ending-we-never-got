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

## Third round: text shading with the golden-halo oval

The user chose the golden-halo oval and asked for more shading behind the
text, never opaque. `sample.py` now captures four shadings, speaker only, on
S004 and S001 (bright), S008 (day, heading and narration) and S023 (night)
into `shading-samples.png` and `shading-detail.png`: A the current shade
(about 55% dark at the text line), B a medium gradient (about 70%), C a
strong gradient (about 82%), D the current shade plus a soft pool behind the
text and a soft shadow around the letters. A first ladder differed too little
to judge and was redrawn before showing.

## Fourth round: the scene's own shadow

The user rejected all four shadings without being sure why (the gradient's
direction, its colour, or a missing top edge). Claude's diagnosis: flat black
turns bright paintings to grey rather than shadow; a featureless full-width
band reads as a technical fix; it darkens where nothing needs it. The samples
now replace the shade with:

1. the painting multiplied by its own shadow colour (the mean colour of its
   darkest fifth in the lower half, about 20% bright; `shadow-tints.json`),
   in the current band shape, so it deepens in its own hue;
2. the same plus soft focus: a blurred copy of the painting behind the text;
3. the same, shaped: deepest behind the portrait and text, fading right and
   up, with a lighter pool under the menu;
4. the same with a fine gilt hairline where the shade begins.

`shadow-samples.png` and `shadow-detail.png`. A first pass came out salmon
pink, too weak, barely blurred and with a stray-looking line; it was redrawn
before showing.

## Fifth round: refined shade and hidden controls

The user found no. 4 (shadow colour, soft focus, shaped, hairline) best but not
perfect: the hairline vanished on the bright S004, the blur wasn't quite nice
enough, and the controls were hard to read; they should be hidden behind a
pop-up and, when open, very elegant.

- The hairline is now engraved: a dark cut beneath a gilt line with a faint
  highlight, so it reads on white marble and in the dark.
- The soft focus is a progressive lens (disc) blur baked for each graded
  painting (`ui/soft/`), done in linear light so highlights bloom, deepening
  toward the text and untouched above the shade, with the painting's grain
  restored so it doesn't look smeared.
- The controls are hidden. A small gilt sun at the lower right opens them; it
  breathes with a soft glow when Look closer is available. Open, they rise over
  a pool of the scene's own blurred shadow, in small capitals (Back, History,
  Look closer when available, Threads, Save, Load, Settings); the item under
  the pointer gains an engraved underline. A click anywhere else closes them
  without turning the page.

`refined-samples.png`, `refined-detail.png` and `controls-detail.png`. The
first capture's pool didn't reach the top items over bright robes; it was
enlarged before showing.
