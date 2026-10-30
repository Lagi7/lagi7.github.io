"""Rebuilds the pictures in img/ from the original art in the Desktop project folders.
Run: python tools/make_images.py   (writes into img/)
"""
import sys, glob, os, random, shutil
from PIL import Image, ImageSequence
O = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")
D = "C:/Users/inzla/OneDrive/Desktop/"
AV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source") + "/"

def key(im, c=None):
    im = im.convert("RGBA"); px = im.load()
    c = c or px[0, 0]
    if len(c) == 4 and c[3] == 0: return im
    w, h = im.size
    for y in range(h):
        for x in range(w):
            if px[x, y][:3] == c[:3]: px[x, y] = (0, 0, 0, 0)
    return im

def row(ims, gap, pad=0, bg=(0, 0, 0, 0), valign="center"):
    W = sum(i.size[0] for i in ims) + gap * (len(ims) - 1) + 2 * pad
    H = max(i.size[1] for i in ims) + 2 * pad
    c = Image.new("RGBA", (W, H), bg); x = pad
    for i in ims:
        y = pad + ((H - 2 * pad - i.size[1]) // 2 if valign == "center" else H - 2 * pad - i.size[1])
        c.paste(i, (x, y), i); x += i.size[0] + gap
    return c

# Avatars
Image.open(AV + "avatar-knight.png").save(O + "/av-knight.png")
m = Image.open(AV + "avatar-mask.jpg").convert("RGB"); w, h = m.size
m.crop(((w - h) // 2, 0, (w - h) // 2 + h, h)).save(O + "/av-mask.jpg", quality=92)

# Houses of Fading Suns
F = D + "FadingSuns/resources/"
U = F + "units/"
t = Image.new("RGBA", (108, 108), (9, 11, 22, 255)); random.seed(11)
for _ in range(46):
    x, y = random.randrange(108), random.randrange(108); v = random.choice([80, 120, 170, 230])
    t.putpixel((x, y), (v, v, min(255, v + 30), 255))
grid = [["air/diringer.png", "space/Dreadnought.png", "air/fighter.png"],
        ["characters/cardinal.png", "characters/knight.png", "characters/inquisitor.png"],
        ["vehicles/plasma cannon.png", "navy/BattleShip.png", "characters/noble.png"]]
for r, rowv in enumerate(grid):
    for c, f in enumerate(rowv):
        s = key(Image.open(U + f)); t.paste(s, (4 + c * 34, 4 + r * 34), s)
t.save(O + "/fs-tile.png")
names = ["space/Dreadnought.png", "space/Crusier.png", "space/lander.png", "air/diringer.png", "air/fighter.png", "navy/BattleShip.png", "navy/Submarine.png",
         "vehicles/plasma cannon.png", "vehicles/armored_train.png", "infantry/crusader.png", "characters/knight.png", "characters/cardinal.png", "characters/inquisitor.png", "characters/noble.png"]
row([key(Image.open(U + n)) for n in names], 4).save(O + "/fs-units.png")
st = [f for f in sorted(glob.glob(F + "structures/*.png"))][:10]
print("structures", [os.path.basename(s) for s in st])
row([key(Image.open(p)) for p in st], 4).save(O + "/fs-structures.png")

# Swantopolk II / Nevsky
N = D + "nevsky/"
mat = Image.open(N + "300 dpi/lord mats/Dietrich_Stepan_300dpi.png").convert("RGB")
W, H = mat.size; mat = mat.crop((int(W * .18), int(H * .5 * .02), int(W * .83), int(H * .5 * .94)))
s = min(mat.size); mat = mat.crop((0, 0, s, s)); mat.thumbnail((900, 900), Image.LANCZOS); mat.save(O + "/nv-mat.jpg", quality=86)
icons = []
for f in ["BOYAR ICON.PNG", "pechche_boyar_icon.PNG", "detiicon.png", "ushkuyniki_icon.png", "kobluki horse icon.png", "light horse icon.png", "militia icon.png", "gorodovy polk red icon.png", "hansa militia_icon.png"]:
    i = Image.open(N + f).convert("RGBA"); i.thumbnail((150, 150), Image.LANCZOS); icons.append(i)
row(icons, 18).save(O + "/nv-icons.png")
cal = Image.open(N + "starting calendar.png").convert("RGB"); cal.thumbnail((1100, 1100), Image.LANCZOS); cal.save(O + "/nv-calendar.jpg", quality=86)
row_ = Image.open(N + "rowing example.png").convert("RGB"); row_.thumbnail((900, 900), Image.LANCZOS); row_.save(O + "/nv-rowing.jpg", quality=86)

# Bitter Heretic
HG = D + "stare z pulpitu/heretic graphics/"
scr = Image.open(AV + "bitter-heretic-screen.webp").convert("RGB")
scr.crop((540, 0, 1606, 1066)).resize((720, 720), Image.LANCZOS).save(O + "/hr-tile.jpg", quality=86)
shutil.copyfile(AV + "bitter-heretic-screen.webp", O + "/hr-screen.webp")
# the Snipping Tool popup in the bottom right is cut off
Image.open(AV + "bitter-heretic-wheel.png").convert("RGB").crop((0, 0, 1520, 1063)).save(O + "/hr-wheel.webp", quality=90)
row([Image.open(HG + "wendigo/" + f).convert("RGBA") for f in ["ICEYH1.png", "ICEYQ1.png", "ICEYH2H8.png"]], 10, valign="bottom").save(O + "/hr-wendigo.png")

# Age of Wonders 1
A = D + "Age of Wonders 1/work age of wonders 1 new graphic/"
ports = [Image.open(A + f).convert("RGBA") for f in ["centaur/123123.bmp", "owl/avatr.bmp", "Leviathan/leviathan_portrait.bmp", "succubus portrait.bmp"]]
tile = Image.new("RGBA", (208, 208), (0, 0, 0, 255))
for k, p in enumerate(ports):
    sq = p.crop((0, 0, 103, 103)); tile.paste(sq, ((k % 2) * 105, (k // 2) * 105))
tile.save(O + "/aow-tile.png")
row(ports, 6).save(O + "/aow-portraits.png")
sp = ["kraken/New Folder2/New Folderasd/kraken1.bmp", "Leviathan/New Folder/leviathan1.bmp", "sunken city/New Folder2/sunken_city1.bmp", "coral reef/New Folder2/reef1.bmp",
      "mushroom farm/New Folder/mushroom farm2.bmp", "shipyard/New Folder2/shipyard1.bmp", "fary dragon/fairydragon/fairydrgn00.bmp", "lizard warrior/final/lizWR101.bmp", "wizard tower/2nd update/WTwr.gif"]
row([key(Image.open(A + f)) for f in sp], 8, valign="bottom").save(O + "/aow-sprites.png")
key(Image.open(A + "Mammoth Logo/mammoth.bmp"), (255, 255, 255)).save(O + "/aow-mammoth.png")
shutil.copyfile(AV + "aow-armored-elephant.gif", O + "/aow-elephant.gif")

# War1gus
WG = D + "stare z pulpitu/archive war1gus/save wa1g/War1gus/contrib/graphics/"
BG = (24, 40, 22, 255)
def crop_gif(src, out, hold_last=0, scale=1):
    g = Image.open(src); fr = [f.convert("RGBA").resize((g.size[0] // 10, g.size[1] // 10), Image.NEAREST) for f in ImageSequence.Iterator(g)]
    dur = g.info.get("duration", 120) or 120
    box = None
    for f in fr:
        b = f.getchannel("A").getbbox()
        if b: box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    p = 2; cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2; s = max(box[2] - box[0], box[3] - box[1]) + 2 * p
    out_frames = []
    for f in fr:
        c = Image.new("RGBA", (s, s), BG); c.paste(f, (s // 2 - cx, s // 2 - cy), f)
        out_frames.append(c.convert("RGB"))
    durs = [dur] * len(out_frames)
    if hold_last: durs[-1] = hold_last
    out_frames[0].save(out + ".gif", save_all=True, append_images=out_frames[1:], duration=durs, loop=0, disposal=1)
    out_frames[0].save(out + ".png")
    print(out.split("/")[-1], len(fr), (s, s), dur)
crop_gif(WG + "units/grunt-alt-shield.gif", O + "/w1-grunt")
crop_gif(WG + "units/sorceress dead.gif", O + "/w1-sorceress", hold_last=1200)
crop_gif(WG + "missiles/hail.gif", O + "/w1-hail")
row([Image.open(WG + "units/" + f).convert("RGBA") for f in ["portrait_sorc3.png", "portrait_sorc4-export.png", "portrait_sorc2.png"]], 4).save(O + "/w1-portraits.png")
row([Image.open(WG + "missiles/" + f).convert("RGBA") for f in ["blood-pool.png", "freeze.png", "blood-footprint.png", "grey_cross.png"]], 8).save(O + "/w1-effects.png")

for f in sorted(os.listdir(O)): print(f, Image.open(O + "/" + f).size, os.path.getsize(O + "/" + f))

# Burning Banners
Image.MAX_IMAGE_PIXELS = None
BB = D + "stare z pulpitu/burning banners/"
lam = Image.open(BB + "lammasu.png").convert("RGBA")
lam.thumbnail((800, 800), Image.LANCZOS); lam.save(O + "/bb-lammasu.webp", quality=85)
card = Image.open(BB + "lammasu.png").convert("RGBA")
w, h = card.size; card = card.crop((0, 0, w // 2, h)); card = card.crop(card.getchannel("A").getbbox())
side = max(card.size) + 60; sq = Image.new("RGBA", (side, side), (43, 36, 51, 255))
sq.paste(card, ((side - card.size[0]) // 2, (side - card.size[1]) // 2), card)
sq.convert("RGB").resize((720, 720), Image.LANCZOS).save(O + "/bb-tile.jpg", quality=86)
icons = []
for f in ["forest icon.png", "icon caster.png", "icon cantrip.png", "icon feral.png", "icon fly.png", "icon huge.png", "icon range.png", "icon reg.png", "icon siege.png", "icon stealth.png"]:
    i = Image.open(BB + "elves/" + f).convert("RGBA"); i.thumbnail((72, 72), Image.LANCZOS); icons.append(i)
row(icons, 16, bg=(0, 0, 0, 255), pad=8).save(O + "/bb-icons.png")

# Cyclades
CY = D + "stare z pulpitu/cyclades/"
ph = Image.open(CY + "black hydra.jpg").convert("RGB"); w, h = ph.size
ph.crop((0, (h - w) // 2, w, (h - w) // 2 + w)).resize((800, 800), Image.LANCZOS).save(O + "/cy-tile.jpg", quality=84)
for src, out in [("croesus.jpg", "cy-croesus.jpg"), ("charo2n.jpg", "cy-charon.jpg")]:
    c = Image.open(CY + src).convert("RGB"); c.thumbnail((520, 760), Image.LANCZOS); c.save(O + "/" + out, quality=86)
a = Image.open(CY + "antigone.jpg").convert("RGB"); a.thumbnail((800, 800), Image.LANCZOS); a.save(O + "/cy-antigone.jpg", quality=86)
for src, out in [("3pvariant.jpg", "cy-3p.jpg"), ("cadet variant.jpg", "cy-cadet.jpg"), ("custom creatures.jpg", "cy-creatures.jpg")]:
    c = Image.open(CY + src).convert("RGB"); c.thumbnail((900, 900), Image.LANCZOS); c.save(O + "/" + out, quality=82)

# Yulin: South China Sea counters (the guide's empty white margin is cut off)
Image.open(AV + "yulin-counter-guide.png").convert("RGB").crop((31, 0, 1043, 447)).save(O + "/scs-counter-guide.webp", quality=92)
Image.open(AV + "yulin-counter-sheet.png").convert("RGB").save(O + "/scs-counter-sheet.webp", quality=92)

# Age of Fantasy: Battalion tile, the right side of the rules page
af = Image.open(AV + "battalion-rules.png").convert("RGBA")
paper = Image.new("RGBA", af.size, (255, 255, 255, 255)); paper.alpha_composite(af)
paper.convert("RGB").crop((152, 0, 941, 789)).resize((720, 720), Image.LANCZOS).save(O + "/af-rules-tile.png", optimize=True)
