"""IMG_4547.mov → wave.png: a sprite sheet of pre-baked ASCII frames (one pixel = one character cell).
pixel value = ramp index * 10 (0 = densest glyph), 255 = background."""
import cv2, numpy as np, json, sys
FLOW = 'NO0A869452I3?!<>=+/:-· '
ROWS = 64                         # character rows: hair to trouser hems (the ground covers the feet)
CELL_ASPECT = 0.5                 # glyph advance / line height
TOP, BOTTOM = 40, 830             # vertical crop in the source (px)
import os
from seg import person_mask
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
CLIP = os.path.join(HERE, "..", "..", "IMG_4547.mov")            # the raw clip lives next to index.html (it is NOT deployed)
cap = cv2.VideoCapture(CLIP); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
assert fr, "could not read " + CLIP
masks = {}

# ── the loop: idle (ping-pong) → raise → wave → [splice] → wave → lower → rest ──
seq = list(range(149, 160, 2)) + list(range(157, 142, -2)) + list(range(145, 241, 2)) + list(range(415, 445, 2))
XF = 4                            # frames cross-faded into the loop start — 437…443, all with the arm already down,
                                  # so the fade never blends a swinging arm with the resting one (that read as two arms)

for i in set(seq): masks[i] = person_mask(fr[i])
union = np.zeros(fr[0].shape[:2], bool)
for i in seq: union |= masks[i] > 0
xs = np.where(union.any(0))[0]
ys_, xs_ = np.where(masks[seq[0]][300:700] > 0); CX = int(np.median(xs_))     # torso centre in the idle pose
half = max(CX - xs.min() + 14, xs.max() - CX + 15)                            # symmetric about the torso: centring the sprite centres Alex
x0, x1 = CX - half, CX + half                                                 # may run past the frame edges; cells() pads those
rh = (BOTTOM - TOP) / ROWS; cw = rh * CELL_ASPECT
COLS = int(np.ceil((x1 - x0) / cw)); x1 = x0 + int(round(COLS * cw))
print("crop x", x0, x1, "(torso centre", CX, ") y", TOP, BOTTOM, "| cell", round(cw, 2), "x", round(rh, 2), "px | grid", COLS, "x", ROWS, "| frames", len(seq))

clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(6, 10))
def cells(i):
    f = np.array(fr[i]); m = (np.array(masks[i]) > 0).astype(np.float32)
    L = cv2.cvtColor(f, cv2.COLOR_BGR2LAB)[..., 0]
    L = clahe.apply(L).astype(np.float32) / 255
    # pad wherever the crop runs past the frame
    pl, pr = max(0, -x0), max(0, x1 - f.shape[1])
    L = np.pad(L, ((0, 0), (pl, pr)), constant_values=1); m = np.pad(m, ((0, 0), (pl, pr)))
    L, m = L[TOP:BOTTOM, x0 + pl:x1 + pl], m[TOP:BOTTOM, x0 + pl:x1 + pl]
    cov = cv2.resize(m, (COLS, ROWS), interpolation=cv2.INTER_AREA)
    lum = cv2.resize(L * m, (COLS, ROWS), interpolation=cv2.INTER_AREA) / np.maximum(cov, 1e-4)   # tone of the person only
    return cov, lum

# tone curve (post-CLAHE luminance → ramp level): black trousers N/O/0, charcoal shirt A/8/6/9, skin 5…?, highlights !<>
CURVE_X = [0.00, 0.10, 0.22, 0.34, 0.46, 0.60, 0.78, 1.00]
CURVE_Y = [0.0,  0.8,  3.0,  5.2,  8.0,  11.0, 14.0, 17.0]
def to_level(cov, lum):
    lvl = np.interp(np.clip(lum, 0, 1), CURVE_X, CURVE_Y)
    edge = np.clip(cov / .8, 0, 1)                                 # partially covered cells thin out → soft silhouette
    return 18 - (18 - lvl) * (.4 + .6 * edge)

raw = [cells(i) for i in seq]
lv = [to_level(c, l) for c, l in raw]; cv_ = [c for c, _ in raw]
# cross-fade the tail into the head so the loop has no seam
for k in range(XF):
    a = (k + 1) / (XF + 1); j = len(seq) - XF + k
    lv[j] = lv[j] * (1 - a) + lv[0] * a; cv_[j] = cv_[j] * (1 - a) + cv_[0] * a
# calm the still areas: a 3-tap temporal filter wherever nothing is really moving (the waving arm stays crisp)
sm = []
for j in range(len(seq)):
    a, b, c = lv[j - 1], lv[j], lv[(j + 1) % len(seq)]
    still = (np.abs(b - a) < 1.6) & (np.abs(c - b) < 1.6)
    sm.append(np.where(still, (a + 2 * b + c) / 4, b))
lv = sm
# quantise with hysteresis so still areas don't boil; two passes so the wrap-around is warm
HYST = .55; prev = None; out = [None] * len(seq)
for p in range(2):
    for j in range(len(seq)):
        q = np.round(lv[j])
        if prev is not None:
            keep = np.abs(lv[j] - prev) < (.5 + HYST); q = np.where(keep, prev, q)
        prev = q; out[j] = q
frames = []
for j in range(len(seq)):
    q = np.clip(out[j], 0, 18).astype(np.uint8) * 10
    q[-2:] = np.minimum(q[-2:], 120)                               # ankles: no wispy glyphs right above the ground
    q[cv_[j] < .2] = 255
    frames.append(q)
frames = np.stack(frames)

PER_ROW = 12; n = len(frames); sheet_rows = int(np.ceil(n / PER_ROW))
sheet = np.full((sheet_rows * ROWS, PER_ROW * COLS), 255, np.uint8)
for j, q in enumerate(frames): r, c = divmod(j, PER_ROW); sheet[r * ROWS:(r + 1) * ROWS, c * COLS:(c + 1) * COLS] = q
cv2.imwrite("wave.png", sheet, [cv2.IMWRITE_PNG_COMPRESSION, 9])
import os; print("wave.png", sheet.shape, os.path.getsize("wave.png"), "bytes")
meta = dict(cols=COLS, rows=ROWS, frames=n, perRow=PER_ROW, fps=round(29 / 2, 2)); json.dump(meta, open("wave.json", "w")); print(meta)
