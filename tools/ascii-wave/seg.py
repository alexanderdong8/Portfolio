"""Cut Alex out of the clip: dark clothes by luminance, skin by Lab a*, then keep only the blob attached to the torso.
Thresholds are tuned to IMG_4547.mov (off-white wall, black clothes); a new clip will need new numbers."""
import cv2, numpy as np
BASE_Y = 744           # top of the baseboard (full-res px)

def person_mask(f):
    """f: BGR 854x480 → uint8 mask (255 = Alex)"""
    lab = cv2.cvtColor(cv2.GaussianBlur(f, (0, 0), 1.0), cv2.COLOR_BGR2LAB).astype(np.int16)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    dark = L < 95
    skin = (a > 135) & (L > 70)
    m = (dark | skin).astype(np.uint8)
    H, W = m.shape
    # below the baseboard line only the legs / feet count
    above = m[BASE_Y - 14:BASE_Y - 2].max(0)                      # leg columns just above the baseboard
    cols = np.where(above > 0)[0]
    cols = cols[(cols > 100) & (cols < 380)]
    lo, hi = (cols.min(), cols.max()) if len(cols) else (150, 320)
    legcols = np.zeros(W, bool); legcols[max(0, lo - 2):hi + 3] = True
    gap = np.where((above == 0) & legcols)[0]                     # the gap between the legs stays open
    legcols[gap] = False
    lower = np.zeros_like(m)
    pants = (L[BASE_Y - 2:] < 60) & legcols[None, :]
    lower[BASE_Y - 2:][pants] = 1
    feetcols = np.zeros(W, bool); feetcols[max(0, lo - 22):hi + 22] = True
    feet = (L[BASE_Y + 50:] > 128) & (a[BASE_Y + 50:] > 134) & feetcols[None, :]
    lower[BASE_Y + 50:][feet] = 1
    m[BASE_Y - 2:] = lower[BASE_Y - 2:]
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    # keep the component(s) attached to the torso
    n, lbl, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    keep = np.zeros_like(m)
    torso = lbl[300:420, 200:260]
    ids = [i for i in np.unique(torso) if i != 0]
    if ids:
        main = max(ids, key=lambda i: stats[i, cv2.CC_STAT_AREA]); keep[lbl == main] = 1
        # feet can be cut off from the pants by a hem shadow: keep foot blobs right under the legs
        for i in range(1, n):
            x, y, w, h, area = stats[i]
            if i != main and y > BASE_Y + 40 and area > 150 and feetcols[min(W - 1, x + w // 2)]: keep[lbl == i] = 1
    keep = cv2.morphologyEx(keep, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    # fill pinholes inside the body
    inv = 1 - keep; n2, l2, s2, _ = cv2.connectedComponentsWithStats(inv.astype(np.uint8), connectivity=4)
    for i in range(1, n2):
        if s2[i, cv2.CC_STAT_AREA] < 120: keep[l2 == i] = 1
    return (keep * 255).astype(np.uint8)
