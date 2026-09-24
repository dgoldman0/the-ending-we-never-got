# Reading panel samples (prototype)

Not part of the game. Samples of the lower reading band as a real surface,
requested by the user on 24 September 2026 after they judged the current
dialogue presentation "not really rich and elegant" and "silly": two framed
heads glancing at each other on every line, gilt frames floating on nothing,
and a gold rule with an arrowhead pointing at the speaker. The text itself was
judged the least problematic part, so it keeps its font and size.

Each sample replaces the dialogue shade with a panel that has one fine
engraved border across its width (two hairlines with beading, broken by the
twelve-ray sun). The speaker's portrait sits in an engraved niche in the
panel; the listener sits in a smaller niche at the far end, across the text.
The name is a rubric above the text, with no pointer. A small lozenge replaces
the continue knot, which read as a (R) sign.

- `lacquer`: deep celadon-black lacquer with gilt engraving.
- `vellum`: warm vellum with gilt and ink engraving and ink text.

Files: `build-panel.py` draws the art in code into `ui/` (not committed;
rebuild it). `zz-panel-prototype.rpy` overrides the stage say screen;
`zz-panel-capture.rpy` holds the capture test cases. `sample.py` builds the
art, copies these into the game only for the capture run, removes them, and
writes `renpy/test-output/review/panel-samples.png` (current, lacquer and
vellum on S004, S002, S008 and S023).

Open questions for the user: the panel is opaque over the bottom 29% of the
screen, where the current shade lets the painting show through; the listener
still appears on every line (showing it only when a reaction matters needs
authoring per line).
