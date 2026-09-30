# ascii-wave

Turns the raw clip of Alex waving (`../../IMG_4547.mov`) into the ASCII figure on the landing page.

    python bake.py   # cut Alex out of the room, bake 74 frames of 63x64 character cells -> wave.png + wave.json
    python wire.py   # embed wave.png into ../../index.html (as a data: URI) and refresh the figure's markup / CSS / JS

Needs `opencv-python` and `numpy`.

- `seg.py` holds the cut-out thresholds. They are tuned to this clip (off-white wall, black clothes): dark
  clothes by luminance, skin by Lab a*, then only the blob attached to the torso is kept, which is what drops
  the outlets, cable, jugs, baseboard and floor.
- `bake.py` assembles the loop (`seq`): idle ping-pong -> raise -> wave -> splice -> lower -> rest, maps tone to
  the site's glyph ramp (`NO0A869452I3?!<>=+/:-`), calms still areas and cross-fades the seam. The crop is
  symmetric about the torso, so centring the sprite centres Alex; the cross-fade only touches frames where the
  arm is already down (blending a swinging arm with the resting one read as two arms).
- One pixel of `wave.png` = one character: value / 10 = ramp level, 255 = empty.

Neither this folder nor the raw clip is deployed (see `.vercelignore`).
