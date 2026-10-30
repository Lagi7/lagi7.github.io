"""Draws the rest of the knight avatar: extends source/avatar-knight.png (60x60, cut off at the
shoulders and chest) to img/av-knight-full.png (76x76) so the armour runs out of the round frame.
Run: python tools/knight_full.py
"""
import os, random
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PAL = {".": (255, 255, 255), "w": (252, 252, 252), "g": (168, 168, 168), "d": (84, 84, 84), "#": (0, 0, 0)}
INV = {v: k for k, v in PAL.items()}
SRC = Image.open(os.path.join(ROOT, "source", "avatar-knight.png")).convert("RGB")
OX, OY, N = 8, 2, 76                      # where the 60x60 sprite sits in the 76x76 canvas
X0, X1, Y1 = -OX, N - OX - 1, N - OY - 1  # sprite coordinates covered by the canvas

px = {}
for y in range(0, Y1 + 1):
    for x in range(X0, X1 + 1):
        px[x, y] = SRC.getpixel((x, y)) if 0 <= x < 60 and y < 60 else None
def put(x, y, c):
    if X0 <= x <= X1 and 0 <= y <= Y1 and px[x, y] is None: px[x, y] = PAL[c]

# outer outline of each shoulder and arm, continuing the curve where the sprite was cut
left_outline = {42: 0, 43: -1, 44: -1, 45: -2, 46: -2, 47: -3, 48: -3, 49: -3}
right_outline = {41: 59, 42: 60, 43: 60, 44: 61, 45: 61, 46: 62, 47: 62, 48: 62, 49: 63}
for y in range(50, Y1 + 1): left_outline[y] = -4; right_outline[y] = 63
# lower edge of each shoulder plate, carried on up to the outline
left_edge = [(-1, 49), (-2, 48), (-1, 50)]
right_edge = [(60, 51), (61, 50), (62, 49), (60, 52)]
# side edges of the breastplate below the sprite
left_side = {60: 6, 61: 5}; right_side = {60: 50, 61: 50}
for y in range(62, Y1 + 1): left_side[y] = 5; right_side[y] = 51

# background beside the helmet, above where each shoulder starts
for y in range(0, min(left_outline)):
    for x in range(X0, 0): put(x, y, ".")
for y in range(0, min(right_outline)):
    for x in range(60, X1 + 1): put(x, y, ".")
for y, x in left_outline.items():
    put(x, y, "#")
    for xx in range(X0, x): put(xx, y, ".")
for y, x in right_outline.items():
    put(x, y, "#")
    for xx in range(x + 1, X1 + 1): put(xx, y, ".")
for x, y in left_edge + right_edge: put(x, y, "#")
for y in range(60, Y1 + 1):
    put(left_side[y], y, "#"); put(right_side[y], y, "#")
    put(left_side[y] + 1, y, "d"); put(right_side[y] - 1, y, "d")       # shadow inside the breastplate edge

# waist and two skirt plates across the bottom of the breastplate
for y, c in ((66, "#"), (67, "g"), (68, "g"), (69, "d"), (70, "#"), (71, "g"), (72, "g"), (73, "d")):
    for x in range(left_side[y] + 1, right_side[y]):
        put(x, y, c)
# central ridge keeps going down the chest
for y in range(60, 66):
    put(28, y, "d"); put(29, y, "d"); put(30, y, "#"); put(31, y, "d"); put(32, y, "d")

# fill whatever is left with plate grey: shadow next to outlines, sparse white rivet speckles
rnd = random.Random(7)
for y in range(0, Y1 + 1):
    for x in range(X0, X1 + 1):
        if px[x, y] is not None: continue
        near_line = any(px.get((x + dx, y + dy)) == PAL["#"] for dx in (-1, 1) for dy in (-1, 0))
        c = "d" if near_line else ("w" if rnd.random() < 0.05 else "g")
        px[x, y] = PAL[c]

out = Image.new("RGB", (N, N), PAL["."])
for (x, y), c in px.items(): out.putpixel((x + OX, y + OY), c)
out.save(os.path.join(ROOT, "img", "av-knight-full.png"))
print("wrote img/av-knight-full.png", out.size)
