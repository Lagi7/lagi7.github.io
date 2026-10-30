"""Draws img/og-card.png, the 1200x630 picture Discord, BGG, Reddit and others show when a link
to lagi7.github.io is pasted. It copies the page header: the two avatars, the name "Łagi" and the motto.

The name is drawn from the same outlines as the <svg class="name-svg"> in page.html, so it matches the
page exactly (the Morpheus font alone has a different Ł and merged A bars).
Run: python tools/og_card.py   (needs Pillow and fonts/Morpheus-7PEV.ttf)
"""
import os, re
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
W, H, SS = 1200, 630, 4                      # card size, supersampling for smooth edges
BG, BG_GLOW = (18, 17, 23), (36, 31, 46)     # --bg and the top glow of body's background
GOLD, GOLD_DIM, BONE, MUTED = (227, 192, 109), (140, 115, 68), (236, 230, 216), (170, 162, 180)


def subpaths(d):
    """Absolute M/L/H/V/Q/Z path data -> list of polygons (quadratic curves flattened)."""
    toks = re.findall(r"[MLHVQZ]|-?\d+(?:\.\d+)?", d)
    polys, cur, cmd, i, x, y = [], [], None, 0, 0.0, 0.0
    while i < len(toks):
        t = toks[i]
        if t in "MLHVQZ":
            cmd = t; i += 1
            if t == "Z":
                if cur: polys.append(cur); cur = []
                continue
            if t == "M" and cur: polys.append(cur); cur = []
            continue
        if cmd in ("M", "L"):
            x, y = float(toks[i]), float(toks[i + 1]); i += 2; cur.append((x, y))
            if cmd == "M": cmd = "L"          # numbers after M are implicit line-tos
        elif cmd == "H": x = float(t); i += 1; cur.append((x, y))
        elif cmd == "V": y = float(t); i += 1; cur.append((x, y))
        elif cmd == "Q":
            cx, cy, ex, ey = (float(v) for v in toks[i:i + 4]); i += 4
            for k in range(1, 9):
                s = k / 8
                cur.append(((1 - s) ** 2 * x + 2 * (1 - s) * s * cx + s * s * ex, (1 - s) ** 2 * y + 2 * (1 - s) * s * cy + s * s * ey))
            x, y = ex, ey
    if cur: polys.append(cur)
    return polys


def fill(polys, size, tf):
    """Even-odd fill of one path into an L mask."""
    m = Image.new("L", size, 0)
    for p in polys:
        one = Image.new("L", size, 0)
        ImageDraw.Draw(one).polygon([tf(px, py) for px, py in p], fill=255)
        m = ImageChops.difference(m, one)    # 0/255 masks, so difference is an XOR
    return m


def name_mask(height):
    """The header's name SVG rendered as a mask `height` pixels tall (before supersampling)."""
    src = open(os.path.join(ROOT, "page.html"), encoding="utf-8").read()
    svg = re.search(r'<svg class="name-svg" viewBox="([-\d ]+)".*?</svg>', src, re.S)
    vx, vy, vw, vh = (float(v) for v in svg.group(1).split())
    k = height * SS / vh
    size = (int(vw * k) + 1, int(vh * k) + 1)
    tf = lambda px, py: ((px - vx) * k, (py - vy) * k)
    body = svg.group(0)
    cut = re.search(r'<mask id="a-gap".*?<path d="([^"]+)" fill="#000"/>', body, re.S).group(1)
    group = re.search(r"<g fill=\"currentColor\">(.*)</g>", body, re.S).group(1)
    out = Image.new("L", size, 0)
    for m in re.finditer(r'<path d="([^"]+)"( mask="url\(#a-gap\)")?/>', group):
        shape = fill(subpaths(m.group(1)), size, tf)
        if m.group(2):                       # the A: cut its original bars out, as the SVG mask does
            shape.paste(0, mask=fill(subpaths(cut), size, tf))
        out = Image.composite(Image.new("L", size, 255), out, shape)
    return out


def avatar(path, d, pixel_art):
    """A round avatar `d` px across with the header's gold ring, on a transparent square."""
    s = d * SS
    ring, gap, dim = round(3 * d / 128) * SS, round(4 * d / 128) * SS, max(1, round(d / 128)) * SS
    full = s + 2 * (gap + dim)
    out = Image.new("RGBA", (full, full), (0, 0, 0, 0))
    dr = ImageDraw.Draw(out)
    dr.ellipse([0, 0, full - 1, full - 1], fill=GOLD_DIM)                          # outer thin ring
    dr.ellipse([dim, dim, full - 1 - dim, full - 1 - dim], fill=BG)               # dark gap
    o = gap + dim
    dr.ellipse([o, o, o + s - 1, o + s - 1], fill=GOLD)                            # gold border
    pic = Image.open(path).convert("RGB")
    inner = s - 2 * ring
    pic = pic.resize((inner, inner), Image.NEAREST if pixel_art else Image.LANCZOS)
    circle = Image.new("L", (inner, inner), 0)
    ImageDraw.Draw(circle).ellipse([0, 0, inner - 1, inner - 1], fill=255)
    out.paste(pic, (o + ring, o + ring), circle)
    return out


def main():
    img = Image.new("RGB", (W * SS, H * SS), BG)
    glow = Image.new("L", (W * SS, H * SS), 0)
    ImageDraw.Draw(glow).ellipse([-W * SS * 0.3, -H * SS * 0.5, W * SS * 1.3, H * SS * 0.5], fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(120 * SS))
    img.paste(Image.new("RGB", img.size, BG_GLOW), mask=glow)
    ImageDraw.Draw(img).rectangle([24 * SS, 24 * SS, (W - 25) * SS, (H - 25) * SS], outline=(58, 52, 69), width=SS)

    # Avatars: knight on top of the gas mask, overlapping like in the header
    d = 220
    knight = avatar(os.path.join(ROOT, "img", "av-knight-design.png"), d, True)
    mask = avatar(os.path.join(ROOT, "img", "av-mask.jpg"), d, False)
    name = name_mask(190)
    overlap = round(14 * d / 128) * SS
    gap = 56 * SS
    group_w = knight.width * 2 - overlap + gap + name.width
    x0 = (W * SS - group_w) // 2
    cy = int(H * SS * 0.5)
    shadow = Image.new("L", img.size, 0)
    for x in (x0, x0 + knight.width - overlap):
        ImageDraw.Draw(shadow).ellipse([x, cy - knight.height // 2 + 18 * SS, x + knight.width, cy + knight.height // 2 + 18 * SS], fill=140)
    img.paste((0, 0, 0), mask=shadow.filter(ImageFilter.GaussianBlur(18 * SS)))
    img.paste(mask, (x0 + knight.width - overlap, cy - mask.height // 2), mask)
    img.paste(knight, (x0, cy - knight.height // 2), knight)

    # Name, with the page's drop shadow and faint gold glow
    nx = x0 + knight.width * 2 - overlap + gap
    ny = cy - 150 * SS
    halo = Image.new("L", img.size, 0); halo.paste(name, (nx, ny))
    img.paste(GOLD, mask=halo.filter(ImageFilter.GaussianBlur(24 * SS)).point(lambda v: v * 46 // 255))
    hard = Image.new("L", img.size, 0); hard.paste(name, (nx, ny + 2 * SS))
    img.paste((0, 0, 0), mask=hard)
    img.paste(GOLD, (nx, ny), name)

    # Motto and address
    dr = ImageDraw.Draw(img)
    morpheus = ImageFont.truetype(os.path.join(ROOT, "fonts", "Morpheus-7PEV.ttf"), 40 * SS)
    dr.text((nx + 4 * SS, ny + name.height + 26 * SS), "Amalgamator of sprites,", font=morpheus, fill=BONE)
    dr.text((nx + 4 * SS, ny + name.height + 76 * SS), "tailor of rules.", font=morpheus, fill=BONE)
    mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22 * SS)
    url = "lagi7.github.io"
    dr.text(((W * SS - dr.textlength(url, font=mono)) // 2, (H - 70) * SS), url, font=mono, fill=MUTED)

    img.resize((W, H), Image.LANCZOS).save(os.path.join(ROOT, "img", "og-card.png"), optimize=True)
    print("wrote img/og-card.png")


if __name__ == "__main__":
    main()
