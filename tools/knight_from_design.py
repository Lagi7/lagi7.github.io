"""Rebuilds the knight avatar from the design screenshot source/avatar-knight-design.png.

The screenshot shows the original 60x60 sprite at about 4x inside the round frame, with the
shoulders and chest finished by hand. Each sprite pixel is read back at its centre and snapped
to the sprite's palette; everything outside the circle is left white.
Run: python tools/knight_from_design.py   (writes img/av-knight-design.png, 74x74)
"""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCALE, OX, OY = 3.98, 92.0, 80.0        # sprite pixel size and sprite origin in the screenshot
X0, Y0, N = -6, -5, 74                  # canvas covers sprite pixels x -6..67, y -5..68 (the circle)
CX, CY, R = 213.7, 209.1, 146.0         # inside of the gold ring in the screenshot
PAL = [(255, 255, 255), (252, 252, 252), (168, 168, 168), (84, 84, 84), (0, 0, 0),
       (252, 84, 84), (168, 84, 84), (252, 168, 0)]

shot = Image.open(os.path.join(ROOT, "source", "avatar-knight-design.png")).convert("RGB")
out = Image.new("RGB", (N, N), PAL[0])
for j in range(N):
    for i in range(N):
        x = OX + (X0 + i + 0.5) * SCALE; y = OY + (Y0 + j + 0.5) * SCALE
        if (x - CX) ** 2 + (y - CY) ** 2 > R ** 2: continue
        c = shot.getpixel((int(x), int(y)))
        out.putpixel((i, j), min(PAL, key=lambda q: sum((a - b) ** 2 for a, b in zip(c, q))))
out.save(os.path.join(ROOT, "img", "av-knight-design.png"))
print("wrote img/av-knight-design.png", out.size)
